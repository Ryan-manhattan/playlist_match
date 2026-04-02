#!/usr/bin/env python3
"""Combine identity tags with lead intent to surface a signal intelligence snapshot."""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDENTITY_PATH = ROOT / 'app' / 'static' / 'data' / 'identity_tags.json'
LEAD_SUMMARY_PATH = ROOT / 'app' / 'static' / 'data' / 'lead_summary.json'
OUTPUT_PATH = ROOT / 'app' / 'static' / 'data' / 'signal_insights.json'


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with path.open('r', encoding='utf-8') as handle:
            return json.load(handle)
    except Exception:
        return {}


def build_signal_insights(identity: dict, lead_summary: dict) -> dict:
    hero_line = identity.get('hero_line') or "Jun의 레이더가 정체성과 수익화 신호 사이를 연결하고 있습니다."
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat()
    if timestamp.endswith('+00:00'):
        timestamp = timestamp.replace('+00:00', 'Z')

    tags = identity.get('tags', [])
    sorted_tags = sorted(tags, key=lambda t: t.get('count', 0), reverse=True)
    top_tags = []
    for entry in sorted_tags[:5]:
        contexts = entry.get('contexts') or []
        context_summary = ' · '.join(contexts[:2])
        if not context_summary:
            context_summary = entry.get('source') or 'culture_rss'
        top_tags.append({
            'tag': entry.get('tag'),
            'count': entry.get('count', 0),
            'context_summary': context_summary,
            'source': entry.get('source')
        })

    keyword_data = lead_summary.get('goal_keywords') or []
    keyword_intents = keyword_data[:6]

    top_keyword_names = [entry.get('keyword') for entry in keyword_intents if entry.get('keyword')]
    if top_keyword_names:
        hero_line = (f"{hero_line} | 이번 주 관심 키워드: {', '.join(top_keyword_names[:3])}. "
                     f"이 신호를 브랜드/멤버십 CTA에 붙여보세요.")

    source_counts = lead_summary.get('top_sources') or []
    source_summary = ', '.join(f"{src['source']} ({src['count']})" for src in source_counts[:3])
    if source_summary:
        hero_line += f" 주요 유입: {source_summary}."

    cta = {
        'label': 'Share signal with Brand Studio',
        'link': '/brand-studio'
    }

    alt_cta = {
        'label': 'Document a Reaction',
        'link': '/diary'
    }

    return {
        'generated_at': timestamp,
        'hero_line': hero_line,
        'top_tags': top_tags,
        'keyword_intents': keyword_intents,
        'cta': cta,
        'alt_cta': alt_cta,
        'notes': 'Refresh signal insights hourly after identity/lead snapshots.'
    }


def save_insights(insights: dict):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', encoding='utf-8') as handle:
        json.dump(insights, handle, ensure_ascii=False, indent=2)


def main():
    identity = _load_json(IDENTITY_PATH)
    lead_summary = _load_json(LEAD_SUMMARY_PATH)
    insights = build_signal_insights(identity, lead_summary)
    save_insights(insights)
    print(f"Signal insights saved ({insights['generated_at']}).")


if __name__ == '__main__':
    main()
