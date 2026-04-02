#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import List, Dict

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / 'app' / 'static' / 'data'
OUTPUT_FILE = DATA_DIR / 'culture_rss.json'

FEEDS = [
    {
        'name': 'NYTimes Arts',
        'url': 'https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml',
        'tagline': '뉴욕타임스 아트 섹션',
        'limit': 3,
    },
    {
        'name': 'NPR Music',
        'url': 'https://www.npr.org/rss/rss.php?id=1039',
        'tagline': 'NPR 뮤직 오프닝',
        'limit': 2,
    },
    {
        'name': 'Rolling Stone Music News',
        'url': 'https://www.rollingstone.com/music/music-news/feed/',
        'tagline': '롤링스톤 최신 커버',
        'limit': 2,
    },
]

HTML_TAG_RE = re.compile(r'<[^>]+>')


def _clean_text(text: str) -> str:
    if not text:
        return ''
    clean = HTML_TAG_RE.sub('', text)
    return ' '.join(clean.split())


def _parse_pubdate(value: str) -> str | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).strftime('%Y-%m-%d')
    except (TypeError, ValueError, IndexError):
        return None


def _gather_entries(feed: Dict) -> List[Dict]:
    try:
        response = requests.get(feed['url'], timeout=12, headers={'User-Agent': 'OffCommunity/1.0'})
        response.raise_for_status()
        root = response.content
    except Exception as exc:
        print(f"[WARN] {feed['name']} fetch failed: {exc}")
        return []

    try:
        import xml.etree.ElementTree as ET
        tree = ET.fromstring(root)
        channel = tree.find('channel')
        if channel is None:
            channel = tree
        items = channel.findall('item')
    except Exception as exc:
        print(f"[WARN] {feed['name']} parse failed: {exc}")
        return []

    gathered = []
    for item in items:
        if len(gathered) >= feed.get('limit', 3):
            break
        title = _clean_text(item.findtext('title') or '')
        link = item.findtext('link') or ''
        description = _clean_text(item.findtext('description') or item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded') or '')
        published = _parse_pubdate(item.findtext('pubDate'))

        if not title and not link:
            continue

        gathered.append({
            'title': title or 'Untitled',
            'link': link,
            'published': published,
            'summary': (description[:180] + '...') if description and len(description) > 180 else description,
        })
    return gathered


def build_payload() -> Dict:
    sources = []
    highlighted_entry = None
    highlighted_source = None

    for feed in FEEDS:
        entries = _gather_entries(feed)
        source_payload = {
            'name': feed['name'],
            'tagline': feed.get('tagline'),
            'entries': entries,
        }
        sources.append(source_payload)

        if not highlighted_entry and entries:
            highlighted_entry = entries[0]
            highlighted_source = source_payload

    if highlighted_entry and highlighted_source:
        summary_line = (
            f"Jun은 요즘 {highlighted_entry['title']} ({highlighted_source['name']})를 읽으며 파트너 리드에 감성을 붙이고 있습니다."
        )
    else:
        summary_line = 'Jun은 일상의 문화 신호를 스캔하며 다음 멤버십/브랜드 스토리를 준비하고 있습니다.'

    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'summary_line': summary_line,
        'sources': sources,
    }
    return payload


def save_payload(payload: Dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open('w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main():
    payload = build_payload()
    save_payload(payload)
    print(f"Culture RSS saved ({len(payload.get('sources', []))} sources) at {payload['generated_at']}")


if __name__ == '__main__':
    main()
