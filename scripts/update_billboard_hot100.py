#!/usr/bin/env python3
"""Fetch the top of the Billboard Hot 100 chart for landing-page storytelling."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import traceback

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT / 'app' / 'static' / 'data' / 'billboard_hot100.json'
CHART_URL = 'https://www.billboard.com/charts/hot-100'
MAX_TRACKS = 5
DEFAULT_PAYLOAD = {
    'source': 'Billboard Hot 100',
    'source_url': CHART_URL,
    'insight_line': 'Billboard Hot 100 신호를 곧 수집합니다.',
    'captured_at': None,
    'top_tracks': [],
}


class BillboardParser:
    """Minimal parser to extract ranking, title, and artist without heavy dependencies."""

    @staticmethod
    def _number_span(li) -> int | None:
        span = li.find('span', class_=lambda cls: cls and 'u-font-size-33' in cls)
        if not span:
            return None
        text = span.get_text(strip=True)
        if not text.isdigit():
            return None
        return int(text)

    @staticmethod
    def _extract_artist(li) -> str:
        span = li.find('span', class_=lambda cls: cls and 'a-no-trucate' in cls)
        if not span:
            return 'Various Artists'
        return span.get_text(strip=True)

    @staticmethod
    def parse(html: str, limit: int = MAX_TRACKS) -> list[dict]:
        soup = BeautifulSoup(html, 'html.parser')
        tracks = []
        current_rank = None
        for item in soup.select('li.o-chart-results-list__item'):
            number = BillboardParser._number_span(item)
            if number is not None and not item.select_one('h3.c-title'):
                current_rank = number
                continue

            title_elem = item.select_one('h3.c-title')
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            artist = BillboardParser._extract_artist(item)
            rank = current_rank or (len(tracks) + 1)
            tracks.append({
                'rank': rank,
                'title': title,
                'artist': artist,
            })
            current_rank = None
            if len(tracks) >= limit:
                break
        return tracks


def fetch_chart_tracks() -> list[dict]:
    resp = requests.get(CHART_URL, headers={'User-Agent': 'Mozilla/5.0'})
    resp.raise_for_status()
    return BillboardParser.parse(resp.text, limit=MAX_TRACKS)


def save(payload: dict):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def build_payload(tracks: list[dict]) -> dict:
    payload = {
        'source': 'Billboard Hot 100',
        'source_url': CHART_URL,
        'insight_line': 'Jun의 레이더는 Billboard Hot 100에 집중합니다.',
        'captured_at': datetime.utcnow().isoformat() + 'Z',
        'top_tracks': tracks,
    }
    return payload


def main():
    try:
        tracks = fetch_chart_tracks()
        if not tracks:
            raise RuntimeError('No tracks parsed from Billboard')
        payload = build_payload(tracks)
        save(payload)
        print(f"Saved Billboard snapshot with {len(tracks)} tracks at {payload['captured_at']}")
    except Exception as exc:  # pragma: no cover - operational script
        print('Failed to fetch Billboard Hot 100 data:')
        traceback.print_exc()
        print('Keeping existing billboard snapshot unchanged.')


if __name__ == '__main__':
    main()
