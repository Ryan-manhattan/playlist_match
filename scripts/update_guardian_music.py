#!/usr/bin/env python3
"""Fetch the latest music coverage from The Guardian's music section."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import traceback

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT / 'app' / 'static' / 'data' / 'guardian_music_feed.json'
SOURCE_URL = 'https://www.theguardian.com/music'
ROOT_URL = 'https://www.theguardian.com'
MAX_ARTICLES = 4
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; GuardianScrape/1.0)'}

DEFAULT_PAYLOAD = {
    'source': 'The Guardian Music Section',
    'source_url': SOURCE_URL,
    'hero_line': 'Jun reads Guardian music dispatches to keep every membership and brand pitch rooted in culture.',
    'generated_at': None,
    'entries': [],
    'notes': 'Hourly autonomous job에서 scripts/update_guardian_music.py를 실행해 Guardian music feed를 갱신하세요.',
}


def _fetch_listing_links() -> list[str]:
    resp = requests.get(SOURCE_URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    container = soup.find('div', id='container-music')
    if not container:
        raise RuntimeError('Guardian music container not found in listing page')

    seen = set()
    links = []
    for li in container.select('li'):
        anchor = li.select_one('a[href^="/music/"]')
        if not anchor:
            continue
        href = anchor['href'].split('#')[0]
        if not href.startswith('/music/'):
            continue
        if href in seen:
            continue
        seen.add(href)
        links.append(href)
        if len(links) >= MAX_ARTICLES:
            break
    return links


def _fetch_article_entry(path: str) -> dict[str, str | None]:
    url = ROOT_URL + path
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    def _meta(prop: str) -> str | None:
        tag = soup.find('meta', property=prop)
        return tag['content'].strip() if tag and tag.has_attr('content') else None

    title = _meta('og:title')
    summary = _meta('og:description')
    published = _meta('article:published_time')
    image = _meta('og:image')
    author_tag = soup.find('meta', attrs={'name': 'author'})
    author = author_tag['content'].strip() if author_tag and author_tag.has_attr('content') else None

    return {
        'title': title,
        'summary': summary,
        'published_at': published,
        'url': url,
        'author': author,
        'image': image,
    }


def build_payload(entries: list[dict]) -> dict:
    payload = {
        **DEFAULT_PAYLOAD,
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'entries': entries,
    }
    return payload


def save(payload: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def main() -> None:
    try:
        paths = _fetch_listing_links()
        entries = []
        for path in paths:
            try:
                entry = _fetch_article_entry(path)
                if entry.get('title'):
                    entries.append(entry)
            except Exception:
                traceback.print_exc()
        if not entries:
            raise RuntimeError('Guardian music entries could not be parsed')
        payload = build_payload(entries)
        save(payload)
        print(f"Saved {len(entries)} Guardian music entries at {payload['generated_at']}")
    except Exception as exc:  # pragma: no cover - operational script
        print('Failed to fetch Guardian music feed:')
        traceback.print_exc()
        print('Keeping existing guardian_music_feed.json unchanged.')


if __name__ == '__main__':
    main()
