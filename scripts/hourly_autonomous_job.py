#!/usr/bin/env python3
"""Coordinate the off-community data refresh pipeline every hour."""

from __future__ import annotations

import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]

PIPELINE_SCRIPTS: List[Tuple[str, Path]] = [
    ("growth summary", ROOT / "scripts" / "update_growth_summary.py"),
    ("promo refresh", ROOT / "scripts" / "update_promo.py"),
    ("Billboard Hot 100", ROOT / "scripts" / "update_billboard_hot100.py"),
    ("Deezer global chart", ROOT / "scripts" / "update_deezer_chart.py"),
    ("Spotify Global Daily", ROOT / "scripts" / "update_spotify_kworb.py"),
    ("culture RSS", ROOT / "scripts" / "update_culture_rss.py"),
    ("Pitchfork signal", ROOT / "scripts" / "update_pitchfork_rss.py"),
    ("identity tags", ROOT / "scripts" / "compile_identity_tags.py"),
    ("identity context feed", ROOT / "scripts" / "compile_identity_context_feed.py"),
    ("Guardian music feed", ROOT / "scripts" / "update_guardian_music.py"),
    ("signal insights", ROOT / "scripts" / "compile_signal_insights.py"),
    ("CTA momentum", ROOT / "scripts" / "compile_cta_momentum.py"),
    ("cultural insights", ROOT / "scripts" / "update_cultural_insights.py"),
    ("culture item build", ROOT / "scripts" / "build_culture_items.py"),
    ("culture items Supabase import", ROOT / "scripts" / "import_culture_items_supabase.py"),
    ("data asset status", ROOT / "scripts" / "log_data_asset_status.py"),
    ("pipeline health", ROOT / "scripts" / "pipeline_health.py"),
]
AUTOMATION_LOG_SCRIPT: Tuple[str, Path] = (
    "automation log snapshot",
    ROOT / "scripts" / "collect_automation_log.py",
)


def _run_script(label: str, script_path: Path) -> Tuple[int, float]:
    start = time.monotonic()
    timestamp = datetime.now(tz=timezone.utc).isoformat()
    if not script_path.exists():
        print(f"[{timestamp}] [SKIP] {label} → missing {script_path}")
        return 1, 0.0

    print(f"[{timestamp}] Running {label} ({script_path.name})")
    try:
        result = subprocess.run([sys.executable, str(script_path)], cwd=ROOT, check=False)
    except Exception as exc:
        duration = time.monotonic() - start
        print(f"[{timestamp}] [ERROR] {label} raised {exc} (after {duration:.1f}s)")
        return 1, duration

    duration = time.monotonic() - start
    status = result.returncode
    tag = "OK" if status == 0 else f"FAIL ({status})"
    print(f"[{timestamp}] [{tag}] {label} finished in {duration:.1f}s")
    return status, duration


def main() -> None:
    print("Hourly autonomous pipeline starting...")
    overall_status = 0
    timeline = []

    for label, script_path in PIPELINE_SCRIPTS:
        status, duration = _run_script(label, script_path)
        if status != 0:
            overall_status = 1
        timeline.append((label, script_path.name, status, duration))

    total_duration = sum(entry[3] for entry in timeline)
    finished_at = datetime.now(tz=timezone.utc).isoformat()

    print("\nPipeline summary:")
    for label, name, status, duration in timeline:
        result_label = "OK" if status == 0 else "FAIL"
        print(f"  • {label} ({name}): {result_label} in {duration:.1f}s")

    print(f"Total duration: {total_duration:.1f}s | finished at {finished_at}")
    print()
    automation_status, _ = _run_script(*AUTOMATION_LOG_SCRIPT)
    if automation_status != 0:
        overall_status = 1

    if overall_status != 0:
        print("One or more scripts failed (see above). Exiting with failure code for scheduler alerting.")
    else:
        print("All steps completed successfully.")

    sys.exit(overall_status)


if __name__ == "__main__":
    main()
