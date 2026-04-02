#!/usr/bin/env python3
"""Fetch the Deezer global chart and persist a snapshot for the landing page."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import traceback

import requests

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT / 'app' / 'static' / 'data' / 'deezer_chart.json'
API_URL = 'https://api.deezer.com/chart/0/tracks'
MAX_TRACKS = 6
HEADERS = {'User-Agent': 'Mozilla/5.0'}

DEFAULT_PAYLOAD = {
    'source': 'Deezer Global Chart',
    'source_url': 'https://www.deezer.com/chart',
    'insight_line': 'Jun의 레이더는 Deezer 글로벌 차트의 감각을 기록하고 있습니다.',
    'captured_at': None,
    'top_tracks': [],
}


def fetch_top_tracks() -> list[dict]:
    resp = requests.get(API_URL, params={'limit': MAX_TRACKS}, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    payload = resp.json()
    entries = payload.get('data') or []
    tracks = []
    for idx, entry in enumerate(entries[:MAX_TRACKS]):
        artist_info = entry.get('artist') or {}
        position = entry.get('position') or (idx + 1)
        popularity = entry.get('rank')
        tracks.append({
            'position': position,
            'title': entry.get('title'),
            'artist': artist_info.get('name') or 'Unknown Artist',
            'duration': entry.get('duration'),
            'popularity': popularity,
        })
    return tracks


def build_payload(tracks: list[dict]) -> dict:
    return {
        'source': 'Deezer Global Chart',
        'source_url': 'https://www.deezer.com/chart',
        'insight_line': 'Jun의 레이더는 Deezer 글로벌 차트의 감각을 기록하고 있습니다.',
        'captured_at': datetime.now(timezone.utc).isoformat(),
        'top_tracks': tracks,
    }


def save(payload: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def main() -> None:
    try:
        tracks = fetch_top_tracks()
        if not tracks:
            raise RuntimeError('No tracks parsed from Deezer chart')
        payload = build_payload(tracks)
        save(payload)
        print(f"Saved Deezer snapshot with {len(tracks)} tracks at {payload['captured_at']}")
    except Exception as exc:  # pragma: no cover - operational script
        print('Failed to fetch Deezer global chart data:')
        traceback.print_exc()
        print('Keeping existing Deezer snapshot unchanged.')


if __name__ == '__main__':
    main()
