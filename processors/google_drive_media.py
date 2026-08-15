"""Google Drive inbox and completed-video helpers for the local publisher."""

from __future__ import annotations

import io
import mimetypes
from pathlib import Path
from typing import Iterable


AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"


class GoogleDriveMediaFolder:
    """Access a single creator-approved Drive folder using the publisher OAuth token."""

    def __init__(self, credentials, folder_id: str, logger=None):
        self.credentials = credentials
        self.folder_id = folder_id
        self.log = logger or print
        self._service_instance = None

    @property
    def service(self):
        if self._service_instance is None:
            from googleapiclient.discovery import build

            self._service_instance = build("drive", "v3", credentials=self.credentials, cache_discovery=False)
        return self._service_instance

    def list_children(self) -> list[dict]:
        """List direct children; this publisher intentionally never scans all of Drive."""
        files: list[dict] = []
        page_token = None
        while True:
            response = self.service.files().list(
                q=f"'{self.folder_id}' in parents and trashed = false",
                fields="nextPageToken,files(id,name,mimeType,createdTime,modifiedTime,size)",
                orderBy="createdTime desc",
                pageSize=100,
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            ).execute()
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken")
            if not page_token:
                return files

    @staticmethod
    def is_audio(item: dict) -> bool:
        return Path(item.get("name", "")).suffix.lower() in AUDIO_EXTENSIONS

    @staticmethod
    def is_image(item: dict) -> bool:
        return Path(item.get("name", "")).suffix.lower() in IMAGE_EXTENSIONS

    def newest_audio_and_cover(self) -> tuple[dict, dict | None]:
        children = self.list_children()
        audio = next((item for item in children if self.is_audio(item)), None)
        if not audio:
            extensions = ", ".join(sorted(AUDIO_EXTENSIONS))
            raise FileNotFoundError(f"No supported audio found in Drive inbox ({extensions})")

        audio_stem = Path(audio["name"]).stem.casefold()
        cover = next(
            (
                item for item in children
                if self.is_image(item) and Path(item["name"]).stem.casefold() == audio_stem
            ),
            None,
        )
        return audio, cover

    def download(self, item: dict, destination_dir: Path) -> Path:
        """Download one approved inbox item to the local render workspace."""
        from googleapiclient.http import MediaIoBaseDownload

        destination_dir.mkdir(parents=True, exist_ok=True)
        filename = Path(item["name"]).name
        destination = destination_dir / f"{item['id']}_{filename}"
        request = self.service.files().get_media(fileId=item["id"], supportsAllDrives=True)
        with io.FileIO(destination, "wb") as handle:
            downloader = MediaIoBaseDownload(handle, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        return destination

    def completed_folder_id(self, name: str = "upload_완료") -> str:
        """Find or create the dedicated output folder inside the approved inbox."""
        for item in self.list_children():
            if item.get("mimeType") == FOLDER_MIME_TYPE and item.get("name") == name:
                return item["id"]

        created = self.service.files().create(
            body={"name": name, "mimeType": FOLDER_MIME_TYPE, "parents": [self.folder_id]},
            fields="id,name,webViewLink",
            supportsAllDrives=True,
        ).execute()
        self.log(f"Created Drive completed folder: {created.get('name')}")
        return created["id"]

    def upload_completed_video(self, video_path: Path, completed_folder_name: str = "upload_완료") -> dict:
        """Store the final MP4 next to the source workflow, only after YouTube succeeds."""
        from googleapiclient.http import MediaFileUpload

        video_path = Path(video_path)
        if not video_path.is_file():
            raise FileNotFoundError(f"Completed video not found: {video_path}")
        mime_type = mimetypes.guess_type(video_path.name)[0] or "video/mp4"
        completed_folder_id = self.completed_folder_id(completed_folder_name)
        response = self.service.files().create(
            body={"name": video_path.name, "parents": [completed_folder_id]},
            media_body=MediaFileUpload(str(video_path), mimetype=mime_type, resumable=True),
            fields="id,name,webViewLink,parents",
            supportsAllDrives=True,
        ).execute()
        return {
            "file_id": response["id"],
            "name": response.get("name", video_path.name),
            "url": response.get("webViewLink"),
            "folder_name": completed_folder_name,
        }

    def move_source_to_completed(self, item: dict, completed_folder_name: str = "upload_완료") -> dict:
        """Move a successfully published source file out of the active inbox."""
        if not item.get("id"):
            raise ValueError("Drive source item must include an id")
        completed_folder_id = self.completed_folder_id(completed_folder_name)
        response = self.service.files().update(
            fileId=item["id"],
            addParents=completed_folder_id,
            removeParents=self.folder_id,
            fields="id,name,webViewLink,parents",
            supportsAllDrives=True,
        ).execute()
        return {
            "file_id": response["id"],
            "name": response.get("name", item.get("name")),
            "url": response.get("webViewLink"),
            "folder_name": completed_folder_name,
        }
