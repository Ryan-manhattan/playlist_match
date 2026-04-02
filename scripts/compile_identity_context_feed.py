#!/usr/bin/env python3
"""Generate a lightweight identity context feed for the landing page."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
IDENTITY_TAGS_PATH = ROOT / 'app' / 'static' / 'data' / 'identity_tags.json'
OUTPUT_PATH = ROOT / 'app' / 'static' / 'data' / 'identity_context_feed.json'

CONTEXT_LIMIT = 170
MAX_CONTEXTS = 6
MAX_TOP_TAGS = 3


def _load_json(path: Path) -> Dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return None


def _excerpt(text: str, limit: int = CONTEXT_LIMIT) -> str:
    clean = text.strip()
    if len(clean) <= limit:
        return clean
    trimmed = clean[:limit]
    if ' ' in trimmed:
        trimmed = trimmed.rsplit(' ', 1)[0]
    return f"{trimmed}…"


def _build_contexts(identity: Dict) -> List[Dict]:
    contexts = []
    seen = set()
    for tag_entry in identity.get('tags', []):
        tag_name = tag_entry.get('tag') or 'Signal'
        tag_count = int(tag_entry.get('count', 0) or 0)
        source = tag_entry.get('source') or 'identity_tags'
        for ctx in tag_entry.get('contexts', []) or []:
            key = (tag_name, ctx)
            if key in seen:
                continue
            seen.add(key)
            contexts.append({
                'tag': tag_name,
                'context': _excerpt(ctx),
                'source': source,
                'tag_count': tag_count,
            })
    if not contexts and identity.get('hero_line'):
        contexts.append({
            'tag': 'Hero',
            'context': _excerpt(identity['hero_line']),
            'source': 'identity_tags',
            'tag_count': len(identity.get('tags', [])),
        })
    contexts.sort(key=lambda item: (-item['tag_count'], len(item['context'])))
    return contexts[:MAX_CONTEXTS]


def _build_top_tags(identity: Dict) -> List[Dict]:
    tags = []
    for tag_entry in identity.get('tags', []):
        tags.append({
            'tag': tag_entry.get('tag', 'Tag'),
            'count': int(tag_entry.get('count', 0) or 0),
            'source': tag_entry.get('source') or 'identity_tags',
        })
    tags.sort(key=lambda item: (-item['count'], item['tag']))
    return tags[:MAX_TOP_TAGS]


def main() -> None:
    identity = _load_json(IDENTITY_TAGS_PATH) or {}
    contexts = _build_contexts(identity)
    top_tags = _build_top_tags(identity)

    feed = {
        'generated_at': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        'headline': identity.get('hero_line') or 'Jun의 정체성 컨텍스트 피드가 갱신되고 있습니다.',
        'summary': identity.get('notes') or 'Identity tags에서 뽑은 맥락을 한 곳에 모아 브랜드/멤버십 CTA로 연결합니다.',
        'top_tags': top_tags,
        'contexts': contexts,
        'cta': {
            'label': 'Share this pulse with Brand Studio',
            'link': '/brand-studio',
        },
        'notes': 'Run scripts/compile_identity_context_feed.py after identity tags refresh to keep this feed alive.',
    }

    OUTPUT_PATH.write_text(json.dumps(feed, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Identity context feed refreshed ({len(contexts)} contexts). Saved to {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
