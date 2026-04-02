#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / 'app' / 'static' / 'data'
OUTPUT_PATH = DATA_DIR / 'data_asset_status.json'


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


def _parse_timestamp(raw: Optional[str]) -> Optional[datetime]:
    if not raw or not isinstance(raw, str):
        return None
    try:
        if raw.endswith('Z'):
            raw = raw.replace('Z', '+00:00')
        return datetime.fromisoformat(raw)
    except ValueError:
        try:
            return datetime.fromisoformat(raw[:26])
        except Exception:
            return None


def _count_list(data: Dict[str, Any], key: str) -> int:
    value = data.get(key)
    if isinstance(value, (list, tuple)):
        return len(value)
    if isinstance(value, dict):
        return len(value)
    return 0


def _sum_lists(data: Dict[str, Any], keys: List[str]) -> int:
    return sum(_count_list(data, key) for key in keys)


ASSET_CONFIGS = [
    {
        'name': 'Culture Pulse',
        'path': DATA_DIR / 'culture.json',
        'time_key': 'updated_at',
        'metric_label': 'signal cards + diaries',
        'metric_fn': lambda data: _sum_lists(data, ['top_tracks', 'film_diaries']),
        'notes': 'scripts/culture_data.py가 공연/다이어리를 큐레이션한 결과입니다.',
    },
    {
        'name': 'Cultural Notes (RSS)',
        'path': DATA_DIR / 'culture_rss.json',
        'time_key': 'generated_at',
        'metric_label': 'source feeds',
        'metric_fn': lambda data: len(data.get('sources', [])) if isinstance(data, dict) else 0,
        'notes': 'NYTimes Arts, NPR Music, Rolling Stone RSS 스냅샷.',
    },
    {
        'name': 'Identity Tags',
        'path': DATA_DIR / 'identity_tags.json',
        'time_key': 'generated_at',
        'metric_label': 'tags',
        'metric_fn': lambda data: len(data.get('tags', [])) if isinstance(data, dict) else 0,
        'notes': 'scripts/compile_identity_tags.py가 RSS 데이터에서 추출했습니다.',
    },
    {
        'name': 'Signal Intelligence',
        'path': DATA_DIR / 'signal_insights.json',
        'time_key': 'generated_at',
        'metric_label': 'top tags',
        'metric_fn': lambda data: len(data.get('top_tags', [])) if isinstance(data, dict) else 0,
        'notes': 'identity + lead signal을 통합하는 scripts/compile_signal_insights.py 결과입니다.',
    },
    {
        'name': 'CTA Momentum',
        'path': DATA_DIR / 'cta_momentum.json',
        'time_key': 'generated_at',
        'metric_label': 'momentum entries',
        'metric_fn': lambda data: len(data.get('entries', [])) if isinstance(data, dict) else 0,
        'notes': 'identity/lead/날씨 신호로 CTA 메시지를 정리합니다.',
    },
    {
        'name': 'Cultural Insights Brief',
        'path': DATA_DIR / 'cultural_insights.json',
        'time_key': 'generated_at',
        'metric_label': 'keywords',
        'metric_fn': lambda data: len(data.get('keywords', [])) if isinstance(data, dict) else 0,
        'notes': 'scripts/update_cultural_insights.py가 RSS+차트 데이터를 요약합니다.',
    },
    {
        'name': 'Lead Pulse',
        'path': DATA_DIR / 'lead_summary.json',
        'time_key': 'generated_at',
        'metric_label': 'total leads',
        'metric_fn': lambda data: int(data.get('total_leads', 0)) if isinstance(data, dict) else 0,
        'notes': 'growth summary 로그로 실시간 리드 집계를 유지합니다.',
    },
    {
        'name': 'Billboard Signal',
        'path': DATA_DIR / 'billboard_hot100.json',
        'time_key': 'captured_at',
        'metric_label': 'hot tracks',
        'metric_fn': lambda data: len(data.get('top_tracks', [])) if isinstance(data, dict) else 0,
        'notes': 'Billboard Hot 100 스냅샷을 기록합니다.',
    },
    {
        'name': 'Deezer Global Pulse',
        'path': DATA_DIR / 'deezer_chart.json',
        'time_key': 'captured_at',
        'metric_label': 'top tracks',
        'metric_fn': lambda data: len(data.get('top_tracks', [])) if isinstance(data, dict) else 0,
        'notes': 'Deezer 글로벌 차트 자료를 저장합니다.',
    },
]


def build_asset_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for config in ASSET_CONFIGS:
        data = _load_json(config['path'])
        updated_at = data.get(config['time_key']) if isinstance(data, dict) else None
        metric_value = None
        if callable(config.get('metric_fn')):
            try:
                metric_value = config['metric_fn'](data)
            except Exception as exc:  # pragma: no cover
                print(f"[WARN] {config['name']} metric 계산 실패: {exc}")
                metric_value = None
        rows.append({
            'name': config['name'],
            'updated_at': updated_at,
            'metric_label': config.get('metric_label'),
            'metric_value': metric_value if metric_value is not None else 0,
            'notes': config.get('notes'),
        })
    rows.sort(key=lambda row: _parse_timestamp(row['updated_at']) or datetime(1970, 1, 1, tzinfo=timezone.utc), reverse=True)
    return rows


if __name__ == '__main__':
    rows = build_asset_rows()
    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'assets': rows,
        'notes': 'Hourly autonomous job에서 scripts/log_data_asset_status.py를 실행해 data_asset_status.json을 갱신하세요.',
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    print(f"Updated data asset status: {OUTPUT_PATH}")
