#!/usr/bin/env python3
"""Render and publish selected Drive audio files with randomly assigned artwork."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INBOX_ID = "1XklZ6JTuaCrUeAxAchlwdmyTAG5MatlS"
DEFAULT_WALLPAPER_FOLDER_ID = "1-T_Mxd8D_FFwOvyN_xrkJCUetz1_Esi-"
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio-id", action="append", required=True, help="Drive file ID of an audio source (repeatable)")
    parser.add_argument("--drive-folder-id", default=DEFAULT_INBOX_ID)
    parser.add_argument("--wallpaper-folder-id", default=DEFAULT_WALLPAPER_FOLDER_ID)
    parser.add_argument("--privacy", choices=("private", "unlisted", "public"), default="private")
    parser.add_argument("--confirm-public", action="store_true")
    parser.add_argument("--force", action="store_true", help="Allow replacing audio already recorded as uploaded")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_env() -> None:
    for raw in (PROJECT_ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            os.environ.setdefault(key, value.strip("'\""))


def clean_title(name: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[_-]+", " ", Path(name).stem)).strip()[:100] or "Untitled track"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    options = args()
    if options.privacy == "public" and not options.confirm_public:
        raise SystemExit("Public publishing requires --confirm-public.")
    load_env()
    sys.path.insert(0, str(PROJECT_ROOT))
    logging.getLogger("dotenv.main").setLevel(logging.ERROR)
    from processors.google_drive_media import GoogleDriveMediaFolder
    from processors.video_processor import VideoProcessor
    from processors.youtube_publisher import YouTubePublisher

    publisher = YouTubePublisher(
        None,
        os.getenv("YOUTUBE_UPLOAD_TOKEN_FILE", str(PROJECT_ROOT / "data" / "youtube_upload_token.json")),
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    )
    if not publisher.configured or not publisher.is_authorized():
        raise SystemExit("YouTube/Drive authorization is required.")

    source_folder = GoogleDriveMediaFolder(publisher._load_credentials(), options.drive_folder_id)
    wallpapers = GoogleDriveMediaFolder(publisher._load_credentials(), options.wallpaper_folder_id)
    audio_by_id = {item["id"]: item for item in source_folder.list_children() if Path(item["name"]).suffix.lower() in AUDIO_EXTENSIONS}
    selected = [audio_by_id[file_id] for file_id in options.audio_id if file_id in audio_by_id]
    missing = set(options.audio_id) - set(audio_by_id)
    if missing:
        raise SystemExit(f"Audio IDs not found in the source folder: {', '.join(sorted(missing))}")
    covers = [item for item in wallpapers.list_children() if Path(item["name"]).suffix.lower() in IMAGE_EXTENSIONS]
    if len(covers) < len(selected):
        raise SystemExit("Not enough wallpaper images for unique assignments.")
    random.SystemRandom().shuffle(covers)
    assignments = list(zip(selected, covers))
    plan = [{"audio": item["name"], "title": clean_title(item["name"]), "wallpaper": cover["name"], "privacy": options.privacy} for item, cover in assignments]
    if options.dry_run:
        print(json.dumps({"success": True, "dry_run": True, "items": plan}, ensure_ascii=False, indent=2))
        return

    root_output = PROJECT_ROOT / "app" / "processed" / "music_publish"
    receipt_file = root_output / "published.jsonl"
    existing_hashes = set()
    if receipt_file.is_file():
        for line in receipt_file.read_text(encoding="utf-8").splitlines():
            try:
                existing_hashes.add(json.loads(line).get("source_sha256"))
            except json.JSONDecodeError:
                pass
    results = []
    for audio_item, cover_item in assignments:
        download_dir = root_output / ".drive_batch" / audio_item["id"]
        audio_path = source_folder.download(audio_item, download_dir)
        source_hash = sha256(audio_path)
        if source_hash in existing_hashes and not options.force:
            results.append({"audio": audio_item["name"], "skipped": True, "reason": "already uploaded (use --force to replace)"})
            continue
        cover_path = wallpapers.download(cover_item, download_dir)
        title = clean_title(audio_item["name"])
        output_dir = root_output / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{source_hash[:10]}"
        output_dir.mkdir(parents=True, exist_ok=False)
        video_path = output_dir / f"{audio_path.stem}.mp4"
        VideoProcessor().create_video_from_audio_image(
            audio_path=str(audio_path), image_path=str(cover_path), output_path=str(video_path),
            video_size=(1920, 1080), fps=30, watermark_title=title,
        )
        youtube = publisher.upload_video(
            str(video_path), title=title, description="Official audio\n\nOFF THE COMMUNITY",
            tags=["official audio", "OFF THE COMMUNITY"], privacy_status=options.privacy, category_id="10",
        )
        completed = source_folder.upload_completed_video(video_path)
        receipt = {
            "published_at": datetime.now(timezone.utc).isoformat(), "source_audio": str(audio_path),
            "source_sha256": source_hash, "title": title, "privacy": options.privacy,
            "video_path": str(video_path), "cover_path": str(cover_path), "youtube_url": youtube["url"],
            "youtube_video_id": youtube["video_id"], "drive_source_file_id": audio_item["id"],
            "drive_completed_video": completed,
        }
        with receipt_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(receipt, ensure_ascii=False, sort_keys=True) + "\n")
        existing_hashes.add(source_hash)
        results.append(receipt)
    print(json.dumps({"success": True, "items": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
