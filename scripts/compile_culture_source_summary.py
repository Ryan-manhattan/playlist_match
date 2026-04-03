#!/usr/bin/env python3
"""Summarize normalized culture items per source for the Culture Source Pulse card."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
NORMALIZED_PATH = ROOT / "data" / "normalized" / "culture_items.jsonl"
OUTPUT_PATH = ROOT / "app" / "static" / "data" / "culture_source_summary.json"

NOTE = (
    "scripts/build_culture_items.py에서 culture RSS·차트 데이터를 정규화한 뒤 "
    "이 스크립트를 실행하면 Culture Source Pulse 카드가 각 소스의 컬렉션 횟수와 최신 수집 시점을 보여줍니다."
)


def _read_items(path: Path) -> Iterable[dict]:
    if not path.exists():
        return ()
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def build_summary() -> dict:
    counts = Counter()
    latest: dict[str, str] = {}
    total = 0

    for item in _read_items(NORMALIZED_PATH):
        source = (item.get("source") or "unknown").strip()
        if not source:
            source = "unknown"
        counts[source] += 1
        total += 1
        collected_at = item.get("collected_at")
        if collected_at:
            current = latest.get(source)
            if not current or collected_at > current:
                latest[source] = collected_at

    source_counts = []
    for source, count in counts.most_common():
        source_counts.append({
            "source": source,
            "count": count,
            "latest_collected_at": latest.get(source),
        })

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_items": total,
        "source_counts": source_counts,
        "notes": NOTE,
    }
    return summary


def save_summary(summary: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def main() -> None:
    summary = build_summary()
    save_summary(summary)
    print(f"Saved culture source summary with {len(summary['source_counts'])} sources (total {summary['total_items']}).")


if __name__ == "__main__":
    main()
