#!/usr/bin/env python3
"""Generate one Lyria 3 music sample and put the MP3 in the OFF Drive inbox."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DRIVE_INBOX_ID = "1XklZ6JTuaCrUeAxAchlwdmyTAG5MatlS"
DEFAULT_PROMPT = (
    "A 30-second contemporary Korean R&B demo at 92 BPM, warm Rhodes chords, "
    "soft sub bass, crisp percussion, dreamy late-night Seoul atmosphere, "
    "female Korean vocals singing a short original hook about a new beginning. "
    "Polished stereo production."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--prompt-file", type=Path, help="Read the Lyria prompt from a UTF-8 text file.")
    parser.add_argument("--model", default="lyria-3-clip-preview")
    parser.add_argument("--output-prefix", default="lyria_sample")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "app" / "processed" / "lyria_samples")
    parser.add_argument("--drive-folder-id", default=DEFAULT_DRIVE_INBOX_ID)
    parser.add_argument("--no-drive-upload", action="store_true")
    return parser.parse_args()


def load_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().removeprefix("export ").strip()
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            os.environ.setdefault(key, value.strip().strip("'\""))


def upload_to_drive(source: Path, folder_id: str) -> dict:
    from googleapiclient.http import MediaFileUpload
    from processors.youtube_publisher import YouTubePublisher

    publisher = YouTubePublisher(
        None,
        os.getenv("YOUTUBE_UPLOAD_TOKEN_FILE", str(PROJECT_ROOT / "data" / "youtube_upload_token.json")),
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    )
    credentials = publisher._load_credentials()
    if credentials is None:
        raise RuntimeError("YouTube/Drive OAuth authorization is required before uploading the sample to Drive.")
    from googleapiclient.discovery import build

    service = build("drive", "v3", credentials=credentials, cache_discovery=False)
    response = service.files().create(
        body={"name": source.name, "parents": [folder_id]},
        media_body=MediaFileUpload(str(source), mimetype="audio/mpeg", resumable=True),
        fields="id,name,webViewLink",
        supportsAllDrives=True,
    ).execute()
    return {"file_id": response["id"], "name": response["name"], "url": response.get("webViewLink")}


def main() -> None:
    options = parse_args()
    load_env()
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY or GOOGLE_API_KEY in the project .env.")

    prompt = options.prompt
    if options.prompt_file:
        prompt = options.prompt_file.expanduser().read_text(encoding="utf-8").strip()
        if not prompt:
            raise SystemExit("The prompt file is empty.")

    sys.path.insert(0, str(PROJECT_ROOT))
    from google import genai

    client = genai.Client(api_key=api_key)
    try:
        interaction = client.interactions.create(model=options.model, input=prompt)
    except Exception as error:
        raise SystemExit(f"Lyria request failed: {error}") from None
    audio = interaction.output_audio
    if not audio or not audio.data:
        raise RuntimeError("Lyria returned no audio data.")

    output_dir = options.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_prefix = re.sub(r"[^A-Za-z0-9_-]+", "_", options.output_prefix).strip("_") or "lyria_sample"
    output_path = output_dir / f"{output_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    output_path.write_bytes(base64.b64decode(audio.data))

    drive_file = None
    if not options.no_drive_upload:
        drive_file = upload_to_drive(output_path, options.drive_folder_id)
    print(json.dumps({
        "success": True,
        "model": options.model,
        "prompt": prompt,
        "audio_path": str(output_path),
        "size_bytes": output_path.stat().st_size,
        "lyrics_or_structure": interaction.output_text,
        "drive_file": drive_file,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
