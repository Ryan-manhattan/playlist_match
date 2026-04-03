#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

ROOT = Path(__file__).resolve().parent.parent
STATIC_DATA_DIR = ROOT / 'app' / 'static' / 'data'
RAW_DIR = ROOT / 'data' / 'raw'
NORMALIZED_DIR = ROOT / 'data' / 'normalized'
DERIVED_DIR = ROOT / 'data' / 'derived'

SOURCES = {
    'culture': STATIC_DATA_DIR / 'culture.json',
    'culture_rss': STATIC_DATA_DIR / 'culture_rss.json',
    'billboard_hot100': STATIC_DATA_DIR / 'billboard_hot100.json',
    'deezer_chart': STATIC_DATA_DIR / 'deezer_chart.json',
}

NORMALIZED_PATH = NORMALIZED_DIR / 'culture_items.jsonl'
DERIVED_PATH = DERIVED_DIR / 'culture_items_latest.json'
MANIFEST_PATH = DERIVED_DIR / 'culture_items_manifest.json'


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open('r', encoding='utf-8') as handle:
            data = json.load(handle)
            return data if isinstance(data, dict) else {}
    except Exception as exc:
        print(f"[WARN] {path.name} 로드 실패: {exc}")
        return {}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def compact_text(value: Optional[str], limit: int = 280) -> Optional[str]:
    if value is None:
        return None
    text = ' '.join(str(value).split())
    if not text:
        return None
    return text[:limit]


def stable_id(parts: Iterable[Any]) -> str:
    joined = '::'.join(str(part or '') for part in parts)
    return hashlib.sha1(joined.encode('utf-8')).hexdigest()[:16]


def make_item(
    *,
    source: str,
    source_type: str,
    title: Optional[str],
    creator: Optional[str] = None,
    url: Optional[str] = None,
    published_at: Optional[str] = None,
    summary: Optional[str] = None,
    tags: Optional[List[str]] = None,
    raw_ref: Optional[str] = None,
    external_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    item_id = stable_id([source, source_type, external_id or title, creator, published_at, url])
    return {
        'id': item_id,
        'source': source,
        'source_type': source_type,
        'external_id': external_id,
        'title': compact_text(title, 220),
        'creator': compact_text(creator, 160),
        'url': url,
        'published_at': published_at,
        'summary': compact_text(summary, 500),
        'tags': tags or [],
        'raw_ref': raw_ref,
        'collected_at': now_iso(),
        'status': 'active',
        'metadata': metadata or {},
    }


def normalize_culture(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for index, track in enumerate(data.get('top_tracks', []) or [], start=1):
        items.append(make_item(
            source='culture',
            source_type='internal_track_snapshot',
            title=track.get('title'),
            creator=track.get('artist'),
            summary=f"internal top track snapshot · wins={track.get('wins', 0)}",
            tags=['music', 'internal', 'snapshot'],
            raw_ref='app/static/data/culture.json',
            external_id=f"culture-track-{index}",
            metadata={'wins': track.get('wins', 0), 'duration': track.get('duration')},
        ))
    for index, diary in enumerate(data.get('film_diaries', []) or [], start=1):
        items.append(make_item(
            source='culture',
            source_type='internal_diary_snapshot',
            title=diary.get('title'),
            creator=diary.get('author'),
            published_at=diary.get('created_at'),
            summary=diary.get('snippet'),
            tags=['film', 'diary', 'internal'],
            raw_ref='app/static/data/culture.json',
            external_id=f"culture-diary-{index}",
        ))
    return items


def normalize_culture_rss(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for source_entry in data.get('sources', []) or []:
        source_name = source_entry.get('name') or 'unknown'
        for index, entry in enumerate(source_entry.get('entries', []) or [], start=1):
            items.append(make_item(
                source='culture_rss',
                source_type='rss_article',
                title=entry.get('title'),
                creator=source_name,
                url=entry.get('link'),
                published_at=entry.get('published'),
                summary=entry.get('summary'),
                tags=['rss', 'culture', source_name.lower().replace(' ', '-')],
                raw_ref='app/static/data/culture_rss.json',
                external_id=f"{source_name}-{index}",
                metadata={'tagline': source_entry.get('tagline')},
            ))
    return items


def normalize_chart(data: Dict[str, Any], *, source: str, rank_key: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for track in data.get('top_tracks', []) or []:
        rank = track.get(rank_key)
        items.append(make_item(
            source=source,
            source_type='chart_track',
            title=track.get('title'),
            creator=track.get('artist'),
            url=data.get('source_url'),
            published_at=data.get('captured_at'),
            summary=f"chart snapshot rank={rank}",
            tags=['music', 'chart', source],
            raw_ref=f"app/static/data/{source}.json",
            external_id=f"{source}-{rank}-{track.get('title')}",
            metadata={
                'rank': rank,
                'popularity': track.get('popularity'),
                'duration': track.get('duration'),
            },
        ))
    return items


def build_items() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    items.extend(normalize_culture(load_json(SOURCES['culture'])))
    items.extend(normalize_culture_rss(load_json(SOURCES['culture_rss'])))
    items.extend(normalize_chart(load_json(SOURCES['billboard_hot100']), source='billboard_hot100', rank_key='rank'))
    items.extend(normalize_chart(load_json(SOURCES['deezer_chart']), source='deezer_chart', rank_key='position'))
    return items


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)

    items = build_items()
    write_jsonl(NORMALIZED_PATH, items)

    payload = {
        'generated_at': now_iso(),
        'count': len(items),
        'sources': sorted({item['source'] for item in items}),
        'items': items[:60],
        'notes': 'Normalized culture items designed for future Supabase table import.',
    }
    manifest = {
        'generated_at': payload['generated_at'],
        'normalized_path': str(NORMALIZED_PATH.relative_to(ROOT)),
        'derived_path': str(DERIVED_PATH.relative_to(ROOT)),
        'schema_version': '1.0',
        'fields': [
            'id', 'source', 'source_type', 'external_id', 'title', 'creator', 'url',
            'published_at', 'summary', 'tags', 'raw_ref', 'collected_at', 'status', 'metadata'
        ],
        'target_table_hint': 'culture_items',
        'count': len(items),
    }

    write_json(DERIVED_PATH, payload)
    write_json(MANIFEST_PATH, manifest)
    print(f"Built normalized culture items: {len(items)} rows")


if __name__ == '__main__':
    main()
