#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'app' / 'static' / 'data'
ASSET_STATUS_PATH = DATA_DIR / 'data_asset_status.json'
OUTPUT_PATH = DATA_DIR / 'pipeline_health.json'

FRESH_WINDOW = timedelta(hours=2)
STALE_WINDOW = timedelta(hours=6)


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open('r', encoding='utf-8') as handle:
            data = json.load(handle)
            return data if isinstance(data, dict) else {}
    except Exception as exc:  # pragma: no cover
        print(f"[WARN] {_sanitize_path(path)} load failed: {exc}")
        return {}


def _sanitize_path(path: Path) -> str:
    return path.name


def _parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value or not isinstance(value, str):
        return None
    normalized = value.strip()
    if normalized.endswith('Z'):
        normalized = normalized[:-1] + '+00:00'
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        try:
            return datetime.fromisoformat(normalized[:26])
        except Exception:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _select_stale_assets(
    assets: List[Dict[str, Any]],
    now: datetime,
) -> Tuple[int, List[Tuple[Dict[str, Any], Optional[datetime]]]]:
    stale: List[Tuple[Dict[str, Any], Optional[datetime]]] = []
    fresh_count = 0
    for asset in assets:
        updated_at = _parse_iso(asset.get('updated_at'))
        if updated_at and updated_at >= now - FRESH_WINDOW:
            fresh_count += 1
        if not updated_at or updated_at < now - STALE_WINDOW:
            stale.append((asset, updated_at))
    stale.sort(key=lambda pair: pair[1] or datetime.min.replace(tzinfo=timezone.utc))
    return fresh_count, stale


def _format_asset(asset: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'name': asset.get('name') or 'Unknown asset',
        'updated_at': asset.get('updated_at'),
    }


def build_pipeline_health() -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    status = _load_json(ASSET_STATUS_PATH)
    assets = status.get('assets', []) if isinstance(status.get('assets'), list) else []
    asset_count = len(assets)

    fresh_count, stale_candidates = _select_stale_assets(assets, now)
    stale_sample = [(_format_asset(asset), added_at) for asset, added_at in stale_candidates]

    asset_times: List[Tuple[Dict[str, Any], datetime]] = []
    for asset in assets:
        updated_at = _parse_iso(asset.get('updated_at'))
        if updated_at:
            asset_times.append((asset, updated_at))

    oldest_asset = None
    if asset_times:
        oldest, _ = min(asset_times, key=lambda pair: pair[1])
        oldest_asset = _format_asset(oldest)
    elif assets:
        oldest_asset = _format_asset(assets[0])

    freshest_asset = None
    if asset_times:
        freshest, _ = max(asset_times, key=lambda pair: pair[1])
        freshest_asset = _format_asset(freshest)

    stale_details = [item[0] for item in stale_sample[:3]]
    fresh_ratio = round((fresh_count / asset_count * 100) if asset_count else 0, 1)

    payload = {
        'generated_at': now.isoformat(),
        'last_run': status.get('generated_at'),
        'asset_count': asset_count,
        'fresh_assets': fresh_count,
        'stale_assets': len(stale_candidates),
        'fresh_ratio': fresh_ratio,
        'thresholds': {
            'fresh_hours': FRESH_WINDOW.total_seconds() / 3600,
            'stale_hours': STALE_WINDOW.total_seconds() / 3600,
        },
        'oldest_asset': oldest_asset,
        'freshest_asset': freshest_asset,
        'stale_details': stale_details,
        'notes': 'Pipeline health summarizes data_asset_status.json so the automation story stays visible.',
    }
    return payload


def main() -> None:
    payload = build_pipeline_health()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    print(f"Pipeline health snapshot saved: {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
