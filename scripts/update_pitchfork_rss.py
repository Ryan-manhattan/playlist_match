#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / 'app' / 'static' / 'data'
OUTPUT_FILE = DATA_DIR / 'pitchfork_rss.json'

FEED_NAME = 'Pitchfork News'
FEED_URL = 'https://pitchfork.com/rss/news/'
ENTRY_LIMIT = 4
HTML_TAG_RE = re.compile(r'<[^>]+>')


def _clean_text(text: str) -> str:
    if not text:
        return ''
    cleaned = HTML_TAG_RE.sub('', text)
    return ' '.join(cleaned.split())


def _parse_pubdate(value: str) -> Optional[str]:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).strftime('%Y-%m-%d')
    except (TypeError, ValueError, IndexError):
        return None


def _fetch_entries() -> List[Dict]:
    try:
        response = requests.get(FEED_URL, timeout=12, headers={'User-Agent': 'OffCommunity/1.0'})
        response.raise_for_status()
        raw = response.content
    except Exception as exc:
        print(f"[WARN] Pitchfork feed fetch failed: {exc}")
        return []

    try:
        import xml.etree.ElementTree as ET
        tree = ET.fromstring(raw)
        channel = tree.find('channel') or tree
        items = channel.findall('item')
    except Exception as exc:
        print(f"[WARN] Pitchfork feed parse failed: {exc}")
        return []

    entries: List[Dict] = []
    for item in items:
        if len(entries) >= ENTRY_LIMIT:
            break
        title = _clean_text(item.findtext('title') or '')
        link = item.findtext('link') or ''
        summary = _clean_text(
            item.findtext('description')
            or item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')
            or ''
        )
        published = _parse_pubdate(item.findtext('pubDate'))
        if not title and not link:
            continue
        entries.append({
            'title': title or 'Untitled',
            'link': link,
            'summary': (summary[:200] + '...') if summary and len(summary) > 200 else summary,
            'published': published,
        })
    return entries


def build_payload() -> Dict:
    entries = _fetch_entries()
    if entries:
        summary_line = (
            f"Pitchfork가 {entries[0]['title']}를 주목하고 있습니다. Jun은 이 신호를 브랜드/멤버십 서사에 녹입니다."
        )
    else:
        summary_line = 'Pitchfork 뉴스를 스캔하며 Jun의 음악 스토리를 최신화하고 있습니다.'

    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'hero_line': 'Pitchfork Signal: Jun의 브랜드 제안에 글로벌 음악 트렌드를 포갭니다.',
        'summary_line': summary_line,
        'source_url': FEED_URL,
        'entries': entries,
        'notes': 'scripts/update_pitchfork_rss.py를 실행해 Pitchfork 뉴스 피드에서 최근 시그널을 기록하세요.',
    }
    return payload


def save_payload(payload: Dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def main() -> None:
    payload = build_payload()
    save_payload(payload)
    print(f"Saved Pitchfork feed with {len(payload.get('entries', []))} entries at {payload['generated_at']}")


if __name__ == '__main__':
    main()
