#!/usr/bin/env python3
"""Summarize the LaunchAgent hourly pipeline log so the UI can show the latest run."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Optional

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = Path("/tmp/off-community-hourly.log")
OUTPUT_PATH = ROOT / "app" / "static" / "data" / "automation_log.json"
MAX_RECENT_LINES = 8


def _read_lines(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        return text.strip().splitlines()
    except Exception:
        return []


def _tail(lines: Iterable[str], limit: int) -> list[str]:
    if not lines:
        return []
    snapshot = list(lines)[-limit:]
    return [line.strip() for line in snapshot if line.strip()]


def _parse_last_run(lines: list[str]) -> str | None:
    for line in reversed(lines):
        if "Total duration" in line and "finished at" in line:
            parts = line.split("finished at", 1)
            if len(parts) > 1:
                return parts[1].strip()
    return None


def _extract_timeline(lines: list[str]) -> list[dict[str, str]]:
    timeline = []
    seen_summary = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("Pipeline summary:"):
            seen_summary = True
            continue
        if not seen_summary:
            continue
        if stripped.startswith("•"):
            content = stripped.lstrip("•").strip()
            if ":" in content:
                label, detail = content.split(":", 1)
            else:
                label, detail = content, ""
            timeline.append({"label": label.strip(), "detail": detail.strip()})
        elif "Total duration" in stripped:
            break
    return timeline


def _detect_status(lines: list[str]) -> tuple[str, str]:
    status = "unknown"
    notes = ""
    for line in reversed(lines):
        if "All steps completed successfully." in line:
            return "success", "All steps completed successfully."
        if "One or more scripts failed" in line:
            return "failed", line.strip()
    return status, notes


def _parse_iso_datetime(value: str | None) -> Optional[datetime]:
    if not value:
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        try:
            parsed = datetime.fromisoformat(normalized[:26])
        except Exception:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _next_expected_run(last_run: str | None) -> dict[str, str] | None:
    parsed = _parse_iso_datetime(last_run)
    if not parsed:
        return None
    next_run = parsed + timedelta(hours=1)
    return {
        "utc": next_run.isoformat(),
        "local": next_run.astimezone().strftime("%Y-%m-%d %H:%M %Z"),
    }


def _build_payload(lines: list[str]) -> dict:
    status, notes = _detect_status(lines)
    last_run = _parse_last_run(lines)
    next_run = _next_expected_run(last_run)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "log_path": str(LOG_PATH),
        "last_run": last_run,
        "next_expected_run_utc": next_run["utc"] if next_run else None,
        "next_expected_run_local": next_run["local"] if next_run else None,
        "status": status,
        "notes": notes or "Batch log capture is available in /tmp/off-community-hourly.log",
        "timeline": _extract_timeline(lines),
        "recent_lines": _tail(lines, MAX_RECENT_LINES),
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "log_path": str(LOG_PATH),
            "last_run": None,
            "next_expected_run_utc": None,
            "next_expected_run_local": None,
            "status": "missing",
            "notes": "Log file not found yet. Run the hourly job once to create it.",
            "timeline": [],
            "recent_lines": [],
        }
    else:
        lines = _read_lines(LOG_PATH)
        payload = _build_payload(lines)
    with OUTPUT_PATH.open("w", encoding="utf-8") as output_file:
        json.dump(payload, output_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
