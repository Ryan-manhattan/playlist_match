#!/usr/bin/env python3
"""Summarize the music analysis sessions for the landing page."""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "music_analysis.db"
OUTPUT_PATH = ROOT / "app" / "static" / "data" / "analysis_summary.json"

NOTE_TEXT = (
    "scripts/update_analysis_summary.py를 실행해 분석 세션 요약을 다시 만들고 "
    "랜딩의 Analysis Summary 카드를 최신 상태로 유지하세요."
)


def _format_rows(rows: Sequence[tuple[str, int]], key_name: str) -> list[dict]:
    formatted = []
    for value, count in rows:
        if not value:
            continue
        formatted.append({key_name: value, "count": count})
    return formatted


def _fetch_rows(cursor: sqlite3.Cursor, query: str, params: Sequence | None = None) -> list[tuple]:
    try:
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except sqlite3.OperationalError:
        return []


def build_summary() -> dict:
    now = datetime.now(timezone.utc).isoformat()
    base = {
        "generated_at": now,
        "session_count": 0,
        "top_genres": [],
        "top_moods": [],
        "top_tags": [],
        "energy_distribution": [],
        "sentiment_summary": {"average": None, "count": 0},
        "recent_sessions": [],
        "notes": NOTE_TEXT,
    }

    if not DB_PATH.exists():
        return base

    conn = sqlite3.connect(str(DB_PATH))
    try:
        cursor = conn.cursor()

        count_row = _fetch_rows(cursor, "SELECT COUNT(*) FROM analysis_sessions")
        if count_row:
            base["session_count"] = count_row[0][0]

        genre_rows = _fetch_rows(
            cursor,
            "SELECT primary_genre, COUNT(*) FROM analysis_sessions "
            "WHERE primary_genre IS NOT NULL AND primary_genre != '' "
            "GROUP BY primary_genre ORDER BY COUNT(*) DESC LIMIT 8",
        )
        base["top_genres"] = _format_rows(genre_rows, "genre")

        mood_rows = _fetch_rows(
            cursor,
            "SELECT primary_mood, COUNT(*) FROM analysis_sessions "
            "WHERE primary_mood IS NOT NULL AND primary_mood != '' "
            "GROUP BY primary_mood ORDER BY COUNT(*) DESC LIMIT 8",
        )
        base["top_moods"] = _format_rows(mood_rows, "mood")

        tag_rows = _fetch_rows(
            cursor,
            "SELECT tag, COUNT(*) FROM video_tags GROUP BY tag ORDER BY COUNT(*) DESC LIMIT 12",
        )
        base["top_tags"] = _format_rows(tag_rows, "tag")

        energy_rows = _fetch_rows(
            cursor,
            "SELECT energy_level, COUNT(*) FROM analysis_sessions "
            "WHERE energy_level IS NOT NULL AND energy_level != '' "
            "GROUP BY energy_level ORDER BY COUNT(*) DESC LIMIT 6",
        )
        base["energy_distribution"] = _format_rows(energy_rows, "energy")

        sentiment_rows = _fetch_rows(
            cursor,
            "SELECT AVG(sentiment_score), COUNT(sentiment_score) FROM analysis_sessions "
            "WHERE sentiment_score IS NOT NULL",
        )
        if sentiment_rows:
            avg, count = sentiment_rows[0]
            if avg is not None:
                base["sentiment_summary"] = {
                    "average": round(avg, 2),
                    "count": int(count or 0),
                }

        recent_rows = _fetch_rows(
            cursor,
            "SELECT video_title, channel_name, artist, song, analyzed_at, sentiment_score "
            "FROM analysis_sessions ORDER BY analyzed_at DESC LIMIT 3",
        )
        latest = []
        for row in recent_rows:
            title, channel, artist, song, analyzed_at, sentiment = row
            latest.append({
                "title": title or "Untitled Session",
                "channel": channel or "Unknown Channel",
                "artist": artist or song or "Unknown Artist",
                "analyzed_at": analyzed_at,
                "sentiment_score": sentiment,
            })
        base["recent_sessions"] = latest

        return base
    finally:
        conn.close()


def save_summary(summary: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)


def main() -> None:
    summary = build_summary()
    save_summary(summary)
    print(f"Analysis summary refreshed ({summary['session_count']} sessions).")


if __name__ == "__main__":
    main()
