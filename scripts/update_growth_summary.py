#!/usr/bin/env python3
"""Aggregate recent growth leads into a lightweight summary JSON for the landing page."""

from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
LEAD_LOG_PATH = ROOT / 'data' / 'growth' / 'growth_leads.jsonl'
SUMMARY_PATH = ROOT / 'app' / 'static' / 'data' / 'lead_summary.json'

LEAD_TYPES = [
    "newsletter",
    "creator_membership",
    "premium_waitlist",
    "brand_partnership",
    "media_kit",
    "insight_report",
]

WORD_PATTERN = re.compile(r"[ㄱ-ㅎ가-힣a-zA-Z0-9]{2,}")
STOPWORDS = {
    "the", "and", "for", "with", "from", "to", "in", "on", "by", "of",
    "정", "된", "하는", "합니다", "하고", "중", "또는", "그", "이", "다",
}


def load_leads() -> list[dict]:
    if not LEAD_LOG_PATH.exists():
        return []

    leads = []
    with LEAD_LOG_PATH.open('r', encoding='utf-8') as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            leads.append(record)
    return leads


def build_summary(leads: list[dict]) -> dict:
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)

    type_counts = Counter({lead_type: 0 for lead_type in LEAD_TYPES})
    recent_counts = Counter({lead_type: 0 for lead_type in LEAD_TYPES})
    source_counts = Counter()
    keyword_counts = Counter()

    for lead in leads:
        lead_type = str(lead.get('lead_type', '')).lower()
        if lead_type in LEAD_TYPES:
            type_counts[lead_type] += 1
        source_page = str(lead.get('source_page', '')).strip().lower() or 'unknown'
        source_counts[source_page] += 1

        created_at = lead.get('created_at')
        if created_at:
            try:
                created_dt = datetime.fromisoformat(created_at)
            except ValueError:
                created_dt = None
            if created_dt and created_dt >= seven_days_ago and lead_type in LEAD_TYPES:
                recent_counts[lead_type] += 1

        goal = str(lead.get('goal', '')).lower()
        for word in WORD_PATTERN.findall(goal):
            if word in STOPWORDS or len(word) < 2:
                continue
            keyword_counts[word] += 1

    top_sources = [
        {"source": source, "count": count}
        for source, count in source_counts.most_common(3)
    ]
    keywords = [
        {"keyword": keyword, "count": count}
        for keyword, count in keyword_counts.most_common(8)
    ]

    return {
        "generated_at": now.isoformat() + 'Z',
        "total_leads": sum(type_counts.values()),
        "lead_types": dict(type_counts),
        "recent_seven_days": sum(recent_counts.values()),
        "recent_leads_by_type": dict(recent_counts),
        "top_sources": top_sources,
        "goal_keywords": keywords,
    }


def save_summary(summary: dict):
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_PATH.open('w', encoding='utf-8') as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)


def main():
    leads = load_leads()
    summary = build_summary(leads)
    save_summary(summary)
    print(f"Lead summary updated, {summary['total_leads']} total leads recorded.")


if __name__ == '__main__':
    main()
