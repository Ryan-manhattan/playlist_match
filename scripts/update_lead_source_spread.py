#!/usr/bin/env python3
"""Build a lead source share snapshot for the home landing page."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'app' / 'static' / 'data'
LEAD_SUMMARY_PATH = DATA_DIR / 'lead_summary.json'
OUTPUT_PATH = DATA_DIR / 'lead_source_spread.json'


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open('r', encoding='utf-8') as handle:
            data = json.load(handle)
            return data if isinstance(data, dict) else {}
    except Exception as exc:  # pragma: no cover
        print(f"[WARN] {path.name} 로드 실패: {exc}")
        return {}


def _normalize_entry(entry: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(entry, dict):
        return None

    source = next(
        (
            str(entry.get(key)).strip()
            for key in ('source', 'name', 'source_name', 'label')
            if entry.get(key)
        ),
        None,
    )
    if not source:
        source = 'unknown'

    raw_count = entry.get('count') or entry.get('value') or entry.get('total') or entry.get('volume')
    try:
        count = int(raw_count) if raw_count is not None else 0
    except (ValueError, TypeError):
        try:
            count = int(float(raw_count))
        except Exception:
            count = 0

    detail = entry.get('detail') or entry.get('notes') or entry.get('description')

    if count <= 0:
        return None

    return {
        'source': source,
        'count': count,
        'detail': str(detail).strip() if detail else None,
    }


def build_lead_source_spread() -> Dict[str, Any]:
    summary = _load_json(LEAD_SUMMARY_PATH)
    total_leads = int(summary.get('total_leads', 0)) if isinstance(summary.get('total_leads'), (int, float)) else 0
    entries = summary.get('top_sources') or []

    aggregated: Dict[str, Dict[str, Any]] = {}
    for raw in entries:
        normalized = _normalize_entry(raw)
        if not normalized:
            continue
        key = normalized['source']
        existing = aggregated.setdefault(key, {'count': 0, 'detail': normalized.get('detail')})
        existing['count'] += normalized['count']
        if normalized.get('detail') and not existing.get('detail'):
            existing['detail'] = normalized['detail']

    sorted_sources = sorted(
        (
            {'source': source, 'count': info['count'], 'detail': info.get('detail')}
            for source, info in aggregated.items()
        ),
        key=lambda row: row['count'],
        reverse=True,
    )

    spread_sources: List[Dict[str, Any]] = []
    running_total = 0
    for row in sorted_sources:
        running_total += row['count']
        percent = round((row['count'] / total_leads) * 100, 1) if total_leads > 0 else 0.0
        spread_sources.append({
            'source': row['source'],
            'count': row['count'],
            'percent': percent,
            'detail': row.get('detail'),
        })

    others_count = max(total_leads - running_total, 0)
    if others_count and total_leads > 0:
        spread_sources.append({
            'source': 'Other sources',
            'count': others_count,
            'percent': round((others_count / total_leads) * 100, 1),
            'detail': 'Remaining leads from low-volume channels',
        })

    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'total_leads': total_leads,
        'sources': spread_sources,
        'notes': 'scripts/update_lead_source_spread.py가 리드 요약에서 유입 소스 점유율을 계산합니다.',
    }
    return payload


def main() -> None:
    payload = build_lead_source_spread()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    print(f"Updated lead source spread: {OUTPUT_PATH} ({len(payload['sources'])} sources)")


if __name__ == '__main__':
    main()
