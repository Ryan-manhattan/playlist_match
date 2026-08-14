import os
import stat
import tempfile
import unittest
from pathlib import Path
from processors.youtube_publisher import YouTubePublisher


class FakeCredentials:
    def to_json(self):
        return '{"token":"test-token"}'


class FakeFlow:
    code_verifier = "pkce-verifier"
    redirect_uri = None

    def authorization_url(self, **kwargs):
        self.authorization_kwargs = kwargs
        return "https://accounts.example.test/authorize", "state-from-provider"


class FakeGrantedCredentials(FakeCredentials):
    def has_scopes(self, scopes):
        return scopes == [
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtube.force-ssl",
            "https://www.googleapis.com/auth/drive",
        ]


class FakeTokenFlow(FakeFlow):
    credentials = FakeGrantedCredentials()

    def fetch_token(self, **kwargs):
        self.fetch_kwargs = kwargs
        self.relaxed_during_fetch = os.environ.get("OAUTHLIB_RELAX_TOKEN_SCOPE")


class YouTubePublisherTests(unittest.TestCase):
    def test_existing_google_client_pair_configures_publisher_without_json_file(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            publisher = YouTubePublisher(
                None,
                str(Path(temporary_directory) / "youtube-token.json"),
                client_id="client-id",
                client_secret="client-secret",
            )

            self.assertTrue(publisher.configured)

    def test_missing_client_pair_and_json_file_is_not_configured(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            publisher = YouTubePublisher(
                str(Path(temporary_directory) / "does-not-exist.json"),
                str(Path(temporary_directory) / "youtube-token.json"),
            )

            self.assertFalse(publisher.configured)

    def test_saved_token_is_replaced_atomically_and_not_world_readable(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            token_file = Path(temporary_directory) / "nested" / "youtube-token.json"
            publisher = YouTubePublisher(None, str(token_file))

            publisher._save_credentials(FakeCredentials())

            self.assertEqual(token_file.read_text(encoding="utf-8"), '{"token":"test-token"}')
            if os.name != "nt":
                self.assertEqual(stat.S_IMODE(token_file.stat().st_mode), 0o600)
            self.assertEqual(list(token_file.parent.glob(f".{token_file.name}.*")), [])

    def test_token_without_drive_scope_is_not_accepted_for_drive_backed_publishing(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            token_file = Path(temporary_directory) / "youtube-token.json"
            token_file.write_text(
                '{"token":"test-token","scopes":["https://www.googleapis.com/auth/youtube.upload"]}',
                encoding="utf-8",
            )
            publisher = YouTubePublisher(None, str(token_file))
            self.assertIsNone(publisher._load_credentials())

    def test_loopback_http_enables_oauthlib_only_for_local_development(self):
        original = os.environ.pop("OAUTHLIB_INSECURE_TRANSPORT", None)
        try:
            YouTubePublisher._allow_localhost_oauth_transport(
                "http://localhost:5000/api/youtube/upload/callback"
            )
            self.assertEqual(os.environ.get("OAUTHLIB_INSECURE_TRANSPORT"), "1")

            os.environ.pop("OAUTHLIB_INSECURE_TRANSPORT", None)
            YouTubePublisher._allow_localhost_oauth_transport(
                "https://example.com/api/youtube/upload/callback"
            )
            self.assertIsNone(os.environ.get("OAUTHLIB_INSECURE_TRANSPORT"))
        finally:
            if original is None:
                os.environ.pop("OAUTHLIB_INSECURE_TRANSPORT", None)
            else:
                os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = original

    def test_authorization_request_returns_pkce_verifier_for_callback_storage(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            publisher = YouTubePublisher(
                None,
                str(Path(temporary_directory) / "youtube-token.json"),
                client_id="client-id",
                client_secret="client-secret",
            )
            flow = FakeFlow()
            publisher._new_flow = lambda: flow

            url, verifier = publisher.authorization_request(
                "http://localhost:5000/api/youtube/upload/callback", "expected-state"
            )

            self.assertEqual(url, "https://accounts.example.test/authorize")
            self.assertEqual(verifier, "pkce-verifier")
            self.assertEqual(flow.redirect_uri, "http://localhost:5000/api/youtube/upload/callback")
            self.assertEqual(flow.authorization_kwargs["state"], "expected-state")
            self.assertNotIn("include_granted_scopes", flow.authorization_kwargs)

    def test_complete_authorization_accepts_scope_superset_and_restores_environment(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            publisher = YouTubePublisher(
                None,
                str(Path(temporary_directory) / "youtube-token.json"),
                client_id="client-id",
                client_secret="client-secret",
            )
            flow = FakeTokenFlow()
            publisher._new_flow = lambda: flow
            original = os.environ.pop("OAUTHLIB_RELAX_TOKEN_SCOPE", None)
            try:
                publisher.complete_authorization(
                    "http://localhost:5000/api/youtube/upload/callback?code=test",
                    "http://localhost:5000/api/youtube/upload/callback",
                    "pkce-verifier",
                )
                self.assertEqual(flow.relaxed_during_fetch, "1")
                self.assertEqual(flow.code_verifier, "pkce-verifier")
                self.assertIsNone(os.environ.get("OAUTHLIB_RELAX_TOKEN_SCOPE"))
            finally:
                if original is not None:
                    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = original


if __name__ == "__main__":
    unittest.main()
