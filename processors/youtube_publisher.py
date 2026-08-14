"""YouTube Data API v3 publishing helpers for generated music videos.

This module deliberately uses an OAuth user credential, not an API key.  API
keys can read public YouTube data but cannot upload to a creator's channel.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import urlsplit


YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
GOOGLE_DRIVE_SCOPE = "https://www.googleapis.com/auth/drive"
# A single operator consent connects the local publisher to both the YouTube
# channel and the designated Drive media inbox/completed-output folder.
GOOGLE_PUBLISHER_SCOPES = [YOUTUBE_UPLOAD_SCOPE, GOOGLE_DRIVE_SCOPE]


class YouTubePublisher:
    """Owns the OAuth token and uploads videos to the connected channel."""

    def __init__(
        self,
        client_secrets_file: Optional[str],
        token_file: str,
        logger: Optional[Callable[[str], None]] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        self.client_secrets_file = Path(client_secrets_file) if client_secrets_file else None
        self.token_file = Path(token_file)
        self.log = logger or print
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def configured(self) -> bool:
        return bool(
            (self.client_secrets_file and self.client_secrets_file.is_file())
            or (self.client_id and self.client_secret)
        )

    def _new_flow(self):
        """Build a Flow from either a downloaded JSON file or environment variables."""
        from google_auth_oauthlib.flow import Flow

        if self.client_secrets_file and self.client_secrets_file.is_file():
            return Flow.from_client_secrets_file(str(self.client_secrets_file), scopes=GOOGLE_PUBLISHER_SCOPES)
        if self.client_id and self.client_secret:
            return Flow.from_client_config({
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                }
            }, scopes=GOOGLE_PUBLISHER_SCOPES)
        raise RuntimeError("YouTube OAuth client credentials are not configured")

    def _load_credentials(self):
        """Load (and, where possible, refresh) the stored user token."""
        if not self.token_file.is_file():
            return None

        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials

        # Credentials.from_authorized_user_file accepts a requested scope list
        # and can make a token look broader than the consent it actually has.
        # Inspect the persisted provider grant before allowing Drive mutations.
        try:
            stored_token = json.loads(self.token_file.read_text(encoding="utf-8"))
            granted_scopes = set(stored_token.get("scopes") or [])
        except (OSError, ValueError, TypeError):
            return None
        if not set(GOOGLE_PUBLISHER_SCOPES).issubset(granted_scopes):
            return None

        credentials = Credentials.from_authorized_user_file(str(self.token_file), GOOGLE_PUBLISHER_SCOPES)
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            self._save_credentials(credentials)
        return credentials if credentials.valid and credentials.has_scopes(GOOGLE_PUBLISHER_SCOPES) else None

    def is_authorized(self) -> bool:
        try:
            return self._load_credentials() is not None
        except Exception:
            # OAuth errors may contain sensitive provider details; callers only
            # need to know that the channel must be reconnected.
            self.log("[YouTubePublisher] Stored token is unusable")
            return False

    def authorization_request(self, redirect_uri: str, state: Optional[str] = None) -> tuple[str, str]:
        """Create the URL plus its PKCE verifier, which must survive the redirect."""
        if not self.configured:
            raise RuntimeError("YouTube OAuth client credentials are not configured")

        self._allow_localhost_oauth_transport(redirect_uri)
        flow = self._new_flow()
        flow.redirect_uri = redirect_uri
        url, _ = flow.authorization_url(
            access_type="offline",
            prompt="consent",
            state=state,
        )
        if not flow.code_verifier:
            raise RuntimeError("OAuth PKCE verifier was not generated")
        return url, flow.code_verifier

    def authorization_url(self, redirect_uri: str, state: Optional[str] = None) -> str:
        """Backwards-compatible URL-only helper for callers that do not use PKCE."""
        url, _ = self.authorization_request(redirect_uri, state)
        return url

    def complete_authorization(
        self,
        authorization_response: str,
        redirect_uri: str,
        code_verifier: Optional[str] = None,
    ) -> None:
        if not self.configured:
            raise RuntimeError("YouTube OAuth client credentials are not configured")
        if not code_verifier:
            raise RuntimeError("OAuth PKCE verifier is missing; start authorization again")

        self._allow_localhost_oauth_transport(redirect_uri)
        flow = self._new_flow()
        flow.redirect_uri = redirect_uri
        flow.code_verifier = code_verifier
        # Google can return a superset of the requested upload scope when the
        # account has prior grants (for example openid/email/profile). oauthlib
        # raises a built-in Warning in that valid case unless explicitly relaxed.
        previous_relaxation = os.environ.get("OAUTHLIB_RELAX_TOKEN_SCOPE")
        os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
        try:
            flow.fetch_token(authorization_response=authorization_response)
        finally:
            if previous_relaxation is None:
                os.environ.pop("OAUTHLIB_RELAX_TOKEN_SCOPE", None)
            else:
                os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = previous_relaxation

        credentials = flow.credentials
        if not credentials.has_scopes(GOOGLE_PUBLISHER_SCOPES):
            raise PermissionError("Google did not grant the required YouTube and Drive publishing scopes")
        self._save_credentials(credentials)

    @staticmethod
    def _allow_localhost_oauth_transport(redirect_uri: str) -> None:
        """Permit OAuth over HTTP only for the standard local loopback callback.

        Google permits loopback redirect URIs during desktop/local development,
        while oauthlib otherwise rejects all HTTP authorization responses. A
        non-local URL is deliberately never relaxed here.
        """
        parsed = urlsplit(redirect_uri)
        if parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
            os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

    def _save_credentials(self, credentials) -> None:
        self.token_file.parent.mkdir(parents=True, exist_ok=True)
        # Write atomically so an upload worker never reads a half-written token.
        temporary_file = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.token_file.parent,
                prefix=f".{self.token_file.name}.",
                delete=False,
            ) as handle:
                temporary_file = Path(handle.name)
                handle.write(credentials.to_json())
            # The token can publish to the connected channel; do not leave it world-readable.
            try:
                os.chmod(temporary_file, 0o600)
            except OSError:
                pass
            os.replace(temporary_file, self.token_file)
        finally:
            if temporary_file and temporary_file.exists():
                try:
                    temporary_file.unlink()
                except OSError:
                    pass

    def upload_video(
        self,
        video_path: str,
        *,
        title: str,
        description: str = "",
        tags: Optional[list[str]] = None,
        privacy_status: str = "private",
        category_id: str = "10",
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> dict:
        """Resumably upload a local MP4 and return its public YouTube URL."""
        if privacy_status not in {"private", "unlisted", "public"}:
            raise ValueError("privacy_status must be private, unlisted, or public")
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        credentials = self._load_credentials()
        if credentials is None:
            raise RuntimeError("YouTube channel is not connected. Complete OAuth authorization first.")

        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        youtube = build("youtube", "v3", credentials=credentials, cache_discovery=False)
        body = {
            "snippet": {
                "title": title[:100],
                "description": description[:5000],
                "tags": (tags or [])[:500],
                "categoryId": str(category_id),
            },
            "status": {"privacyStatus": privacy_status, "selfDeclaredMadeForKids": False},
        }
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=MediaFileUpload(video_path, chunksize=8 * 1024 * 1024, resumable=True),
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status is not None and progress_callback:
                progress_callback(int(status.progress() * 100), "YouTube에 업로드 중...")

        video_id = response.get("id")
        if not video_id:
            raise RuntimeError(f"YouTube did not return a video id: {json.dumps(response)}")
        return {
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "privacy_status": privacy_status,
        }
