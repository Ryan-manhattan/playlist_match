#!/usr/bin/env python3
"""Push normalized culture items into Supabase for long-term archival."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

from utils import app_settings
from utils.supabase_client import SupabaseClient

ROOT = Path(__file__).resolve().parents[1]
NORMALIZED_PATH = ROOT / 'data' / 'normalized' / 'culture_items.jsonl'
MANIFEST_PATH = ROOT / 'data' / 'derived' / 'culture_items_manifest.json'
CHUNK_SIZE = 120


def load_manifest() -> Dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {}

    try:
        with MANIFEST_PATH.open('r', encoding='utf-8') as handle:
            return json.load(handle)
    except Exception as exc:
        print(f"[WARN] manifest load failed: {exc}")
        return {}


def load_items() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []

    if not NORMALIZED_PATH.exists():
        return items

    with NORMALIZED_PATH.open('r', encoding='utf-8') as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"[WARN] malformed line in {NORMALIZED_PATH.name}: {exc}")

    return items


def chunked(rows: List[Dict[str, Any]], size: int) -> Iterable[List[Dict[str, Any]]]:
    for i in range(0, len(rows), size):
        yield rows[i:i + size]


def supabase_configured() -> bool:
    return bool(app_settings.SUPABASE_URL and app_settings.SUPABASE_KEY)


def execute_upsert(table, chunk: List[Dict[str, Any]]):
    builder = table.insert(chunk)
    if hasattr(builder, 'on_conflict'):
        builder = builder.on_conflict('id')
    return builder.execute()


def main() -> None:
    if not NORMALIZED_PATH.exists():
        print(f"[SKIP] {NORMALIZED_PATH.name} missing, nothing to import")
        return

    items = load_items()
    if not items:
        print(f"[SKIP] No normalized culture items to import")
        return

    manifest = load_manifest()
    print(f"[INFO] {len(items)} culture items ready (schema {manifest.get('schema_version', 'unknown')})")

    if not supabase_configured():
        print("[SKIP] Supabase not configured (SUPABASE_URL/SUPABASE_KEY missing)")
        return

    try:
        client = SupabaseClient()
    except Exception as exc:
        print(f"[SKIP] Supabase client unavailable: {exc}")
        return

    table = client.client.table('culture_items')

    try:
        table.select('id').limit(1).execute()
    except Exception as exc:
        message = str(exc).lower()
        if 'does not exist' in message or 'relation' in message:
            print("[SKIP] culture_items table not found in Supabase")
            return
        raise

    success_count = 0

    for chunk in chunked(items, CHUNK_SIZE):
        try:
            result = table.upsert(chunk, on_conflict='id').execute()
        except AttributeError:
            result = execute_upsert(table, chunk)
        except Exception as exc:
            print(f"[ERROR] Supabase culture_items import failed: {exc}")
            sys.exit(1)

        error_payload = getattr(result, 'error', None)
        if error_payload:
            print(f"[ERROR] Supabase reported an error: {error_payload}")
            sys.exit(1)

        success_count += len(chunk)
        print(f"[INFO] Upserted {len(chunk)} rows (total so far: {success_count})")

    print(f"[OK] Supabase culture_items import complete ({success_count} rows)")


if __name__ == '__main__':
    main()
