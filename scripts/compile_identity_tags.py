#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'app' / 'static' / 'data'
CULTURE_RSS_PATH = DATA_DIR / 'culture_rss.json'
OUTPUT_PATH = DATA_DIR / 'identity_tags.json'

STOPWORDS = {
    'the', 'and', 'for', 'with', 'from', 'that', 'this', 'what', 'when', 'your',
    'jun', 'culture', 'music', 'notes', 'signal', 'signals', 'review', 'new', 'latest',
    'live', 'global', 'will', 'are', 'is', 'in', 'on', 'of', 'to', 'by', 'as', 'it',
    'or', 'at', 'an', 'be', 'has', 'her', 'his', 'per', 'via', 'but', 'not', 'into',
    'from', 'a', 'the', 'i', 'we', 'you', 'she', 'he', 'they', 'them', 'our', 'its'
}
TOKEN_RE = re.compile(r"[A-Za-z0-9\uac00-\ud7a3']{3,}")


def tokenize(value: str) -> list[str]:
    tokens = []
    if not value:
        return tokens
    for match in TOKEN_RE.finditer(value.lower()):
        token = match.group(0)
        if token in STOPWORDS:
            continue
        if token.isnumeric():
            continue
        tokens.append(token)
    return tokens


def load_culture_entries() -> tuple[str, list[dict[str, str]]]:
    if not CULTURE_RSS_PATH.exists():
        return '', []

    with CULTURE_RSS_PATH.open('r', encoding='utf-8') as f:
        data = json.load(f)

    summary_line = str(data.get('summary_line', '') or '')
    sources = data.get('sources') or []
    entries = []

    for source in sources:
        source_name = source.get('name') or source.get('tagline') or 'culture'
        for entry in source.get('entries') or []:
            combined = ' '.join(filter(None, [entry.get('title'), entry.get('summary')]))
            if not combined.strip():
                continue
            entries.append({
                'text': combined,
                'context_label': f"{source_name}: {entry.get('title', 'Untitled')}"
            })
    return summary_line, entries


def build_identity_tags(summary_line: str, entries: Iterable[dict[str, str]]) -> dict:
    counter = Counter()
    contexts = defaultdict(list)

    data_points = []
    if summary_line:
        data_points.append((summary_line, 'Summary line'))
    data_points.extend((item['text'], item['context_label']) for item in entries)

    for text, label in data_points:
        for token in tokenize(text):
            counter[token] += 1
            if label and len(contexts[token]) < 2 and label not in contexts[token]:
                contexts[token].append(label)

    common = counter.most_common(6)
    tags = []
    for token, freq in common:
        display = token.capitalize()
        tags.append({
            'tag': display,
            'count': freq,
            'contexts': contexts.get(token, []),
            'source': 'culture_rss'
        })

    hero_line = summary_line or 'Jun의 문화 레이더가 새로운 감성 태그를 기록하고 있습니다.'
    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'hero_line': hero_line,
        'tags': tags,
        'notes': 'Derived from culture_rss snapshots. Run scripts/compile_identity_tags.py to refresh.'
    }


def main() -> None:
    summary_line, entries = load_culture_entries()
    identity = build_identity_tags(summary_line, entries)

    with OUTPUT_PATH.open('w', encoding='utf-8') as f:
        json.dump(identity, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(identity['tags'])} identity tags to {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
