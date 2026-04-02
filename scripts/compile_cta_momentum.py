#!/usr/bin/env python3
"""Generate CTA momentum insights from identity tags + lead intents."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
IDENTITY_PATH = ROOT / 'app' / 'static' / 'data' / 'identity_tags.json'
LEAD_SUMMARY_PATH = ROOT / 'app' / 'static' / 'data' / 'lead_summary.json'
OUTPUT_PATH = ROOT / 'app' / 'static' / 'data' / 'cta_momentum.json'
WEATHER_URL = 'https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current_weather=true'
WORD_PATTERN = re.compile(r"[ㄱ-ㅎ가-힣a-zA-Z0-9]{2,}")
STOPWORDS = {
    "the", "and", "for", "with", "from", "to", "in", "on", "by", "of",
    "Jun", "jun", "감성", "추구", "전달", "기반", "전문", "브랜드", "musical"
}

LEAD_TYPE_LABELS = {
    "newsletter": "Founder List",
    "creator_membership": "Creator Membership",
    "premium_waitlist": "Premium Waitlist",
    "brand_partnership": "Brand Partnership",
    "media_kit": "Media Kit",
    "insight_report": "Audience Insight Report",
}

CTA_TEMPLATES = {
    "brand_partnership": {"label": "Request Brand Call", "link": "/brand-studio"},
    "insight_report": {"label": "Request Insight Report", "link": "/brand-studio"},
    "media_kit": {"label": "Request Media Kit", "link": "/brand-studio"},
    "creator_membership": {"label": "Share Your Archive", "link": "/playlists"},
    "premium_waitlist": {"label": "Apply for Founders", "link": "/diary"},
    "newsletter": {"label": "Join Founder List", "link": "/diary"},
    "default": {"label": "Share Signal with Brand Studio", "link": "/brand-studio"},
}

WEATHER_CODE_LABELS = {
    0: 'Clear Skies',
    1: 'Mainly Clear',
    2: 'Partly Cloudy',
    3: 'Overcast',
    45: 'Foggy',
    48: 'Fog with Ice',
    51: 'Light Drizzle',
    53: 'Moderate Drizzle',
    55: 'Dense Drizzle',
    56: 'Light Freezing Drizzle',
    57: 'Dense Freezing Drizzle',
    61: 'Light Rain',
    63: 'Moderate Rain',
    65: 'Heavy Rain',
    66: 'Light Freezing Rain',
    67: 'Dense Freezing Rain',
    71: 'Light Snow',
    73: 'Moderate Snow',
    75: 'Heavy Snow',
    80: 'Rain Showers',
    81: 'Moderate Rain Showers',
    82: 'Violent Rain Showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with Hail',
    99: 'Thunderstorm with Heavy Hail',
}

FALLBACK_KEYWORDS = [
    {"keyword": "contextual storytelling", "count": 1},
    {"keyword": "emotional data", "count": 1},
    {"keyword": "vibe research", "count": 1},
]


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with path.open('r', encoding='utf-8') as handle:
            return json.load(handle)
    except Exception:
        return {}


def fetch_weather_context() -> str | None:
    try:
        resp = requests.get(WEATHER_URL, timeout=8)
        resp.raise_for_status()
        payload = resp.json()
        current = payload.get('current_weather') or {}
        temp = current.get('temperature')
        code = current.get('weathercode')
        description = WEATHER_CODE_LABELS.get(code, 'Brisk Pulse')
        if temp is None:
            return None
        return f"Seoul {temp:.1f}°C · {description}"
    except Exception:
        return None


def extract_context_keywords(identity: dict, limit: int = 6) -> list[str]:
    contexts = []
    for tag in identity.get('tags', []):
        contexts.extend(tag.get('contexts') or [])
    words = []
    for context in contexts:
        matches = WORD_PATTERN.findall(context)
        words.extend([match.lower() for match in matches])
    filtered = [word for word in words if word not in STOPWORDS]
    return filtered[:limit]


def build_keywords(lead_summary: dict, identity: dict) -> list[dict]:
    keywords = lead_summary.get('goal_keywords', []) or []
    if keywords:
        return keywords[:6]

    candidates = extract_context_keywords(identity, limit=12)
    if candidates:
        counter = Counter(candidates)
        return [{"keyword": keyword, "count": count} for keyword, count in counter.most_common(6)]

    return FALLBACK_KEYWORDS.copy()


def select_lead_type(lead_summary: dict) -> str:
    recent = lead_summary.get('recent_leads_by_type') or {}
    if recent:
        best = max(recent.items(), key=lambda entry: entry[1])
        if best[1] > 0:
            return best[0]
    totals = lead_summary.get('lead_types') or {}
    if totals:
        best = max(totals.items(), key=lambda entry: entry[1])
        if best[1] > 0:
            return best[0]
    return 'brand_partnership'


def build_context_line(weather_line: str | None, lead_summary: dict, intent_label: str) -> str:
    parts: list[str] = []
    if weather_line:
        parts.append(weather_line)
    sources = lead_summary.get('top_sources') or []
    if sources:
        source_line = ', '.join(f"{entry.get('source', 'source')} ({entry.get('count', 0)})" for entry in sources[:3])
        parts.append(f"Top sources: {source_line}")
    if not parts:
        return f"{intent_label} signals are being compiled for the next CTA push."
    parts.append(f"Signals lean toward {intent_label.lower()}.")
    return ' · '.join(parts)


def build_entries(identity: dict, keywords: list[dict], lead_label: str, lead_type: str) -> list[dict]:
    tags = sorted(identity.get('tags', []), key=lambda entry: entry.get('count', 0), reverse=True)
    if not tags:
        tags = [{"tag": "Jun", "count": 0, "contexts": []}]

    entries = []
    zipped = list(zip(tags, keywords))
    for tag_entry, keyword_entry in zipped[:3]:
        tag_label = tag_entry.get('tag') or 'Jun'
        contexts = tag_entry.get('contexts') or []
        context_hint = contexts[0] if contexts else 'culture notes'
        keyword_label = keyword_entry.get('keyword') or 'signal'
        message = (
            f"{tag_label} 감성과 '{keyword_label}' 키워드가 {lead_label} 문의를 자극하는 신호를 만들고 있습니다. "
            f"{context_hint}에서 힘을 얻은 제안으로 CTA를 강화하세요."
        )
        entry = {
            'tag': tag_label,
            'tag_count': tag_entry.get('count', 0),
            'keyword': keyword_label,
            'keyword_count': keyword_entry.get('count', 0),
            'intent_label': lead_label,
            'message': message,
            'cta': CTA_TEMPLATES.get(lead_type, CTA_TEMPLATES['default']).copy(),
        }
        entries.append(entry)

    if not entries:
        fallback_tag = tags[0]
        fallback_keyword = keywords[0] if keywords else {'keyword': 'signal moment', 'count': 0}
        entry = {
            'tag': fallback_tag.get('tag', 'Jun'),
            'tag_count': fallback_tag.get('count', 0),
            'keyword': fallback_keyword.get('keyword', 'signal moment'),
            'keyword_count': fallback_keyword.get('count', 0),
            'intent_label': lead_label,
            'message': f"{fallback_tag.get('tag', 'Jun')} 태그와 '{fallback_keyword.get('keyword', 'signal moment')}'가 새로운 CTA를 지탱할 리드로 파고들고 있습니다.",
            'cta': CTA_TEMPLATES.get(lead_type, CTA_TEMPLATES['default']).copy(),
        }
        entries.append(entry)

    return entries


def build_payload(entries: list[dict], context_line: str) -> dict:
    now = datetime.now(timezone.utc)
    iso = now.isoformat().replace('+00:00', 'Z')
    return {
        'generated_at': iso,
        'context_line': context_line,
        'entries': entries,
        'notes': 'Run scripts/compile_cta_momentum.py hourly after identity/lead snapshots.',
    }


def save_payload(payload: dict):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def main():
    identity = _load_json(IDENTITY_PATH)
    lead_summary = _load_json(LEAD_SUMMARY_PATH)

    weather_line = fetch_weather_context()
    keywords = build_keywords(lead_summary, identity)
    lead_type = select_lead_type(lead_summary)
    lead_label = LEAD_TYPE_LABELS.get(lead_type, LEAD_TYPE_LABELS['brand_partnership'])
    entries = build_entries(identity, keywords, lead_label, lead_type)
    context_line = build_context_line(weather_line, lead_summary, lead_label)
    payload = build_payload(entries, context_line)
    save_payload(payload)
    print(f"CTA momentum saved ({payload['generated_at']}).")


if __name__ == '__main__':
    main()
