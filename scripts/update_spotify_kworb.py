#!/usr/bin/env python3
"""Pull Spotify "Global Daily" rankings from Kworb and persist a JSON snapshot."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "app" / "static" / "data" / "spotify_daily_chart.json"
CHART_URL = "https://kworb.net/spotify/country/global_daily.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
MAX_TRACKS = 6


def _to_int(value: str) -> int:
    if value is None:
        return 0
    text = value.replace("\xa0", " ").replace(",", "").strip()
    if not text:
        return 0
    sign = 1
    if text[0] == "+":
        text = text[1:]
    elif text[0] == "-":
        sign = -1
        text = text[1:]
    try:
        return sign * int(text)
    except ValueError:  # pragma: no cover
        return 0


def _clean_text(value: str) -> str:
    return " ".join(value.split()) if isinstance(value, str) else ""


def fetch_top_tracks() -> List[Dict[str, str]]:
    response = requests.get(CHART_URL, headers=HEADERS, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "spotifydaily"})
    if not table:
        raise RuntimeError("Spotify daily table not found")

    rows = table.find("tbody").find_all("tr")
    tracks = []
    for row in rows[:MAX_TRACKS]:
        cells = row.find_all("td")
        if len(cells) < 11:
            continue

        position = _to_int(cells[0].get_text())
        artist_cell = cells[2]
        anchors = artist_cell.find_all("a")
        artist = anchors[0].get_text(strip=True) if anchors else _clean_text(artist_cell.get_text())
        title = anchors[-1].get_text(strip=True) if anchors else ""
        link = anchors[-1]["href"] if anchors and anchors[-1].has_attr("href") else ""
        if link and not link.startswith("http"):
            link = f"https://kworb.net/spotify/{link.lstrip('./') if link.startswith('./') else link.lstrip('..')}"

        tracks.append({
            "rank": position,
            "artist": artist,
            "title": title,
            "link": link,
            "days_on_chart": _to_int(cells[3].get_text()),
            "peak_position": _to_int(cells[4].get_text()),
            "peak_multiplier": _clean_text(cells[5].get_text()),
            "daily_streams": _to_int(cells[6].get_text()),
            "daily_change": _to_int(cells[7].get_text()),
            "weekly_streams": _to_int(cells[8].get_text()),
            "weekly_change": _to_int(cells[9].get_text()),
            "total_streams": _to_int(cells[10].get_text()),
        })

    return tracks


def main() -> None:
    tracks = fetch_top_tracks()
    payload = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "source_url": CHART_URL,
        "notes": "scripts/update_spotify_kworb.py captures Kworb's Global Daily Spotify chart for Jun's radar.",
        "top_tracks": tracks,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    print(f"Spotify chart snapshot saved to {OUTPUT_PATH} with {len(tracks)} tracks.")


if __name__ == "__main__":
    main()
