#!/usr/bin/env python3
"""Build the mobile home payload from the current website data assets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
MOBILE_PAYLOAD_PATH = REPO_ROOT / "apps/mobile/assets/data/home_payload.json"


def load_json(relative_path: str) -> dict[str, Any]:
    path = REPO_ROOT / relative_path
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def compact_value(value: Any) -> str:
    try:
        number = int(value)
    except Exception:
        return str(value or "")

    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    if number >= 1_000:
        return f"{number / 1_000:.1f}K"
    return str(number)


def build_payload() -> dict[str, Any]:
    cultural_insights = load_json("app/static/data/cultural_insights.json")
    culture_rss = load_json("app/static/data/culture_rss.json")
    identity_tags = load_json("app/static/data/identity_tags.json")
    identity_context = load_json("app/static/data/identity_context_feed.json")
    signal_insights = load_json("app/static/data/signal_insights.json")
    cta_momentum = load_json("app/static/data/cta_momentum.json")
    promo = load_json("app/static/data/promo.json")
    lead_summary = load_json("app/static/data/lead_summary.json")
    billboard = load_json("app/static/data/billboard_hot100.json")
    deezer = load_json("app/static/data/deezer_chart.json")
    spotify = load_json("app/static/data/spotify_daily_chart.json")
    data_asset_status = load_json("app/static/data/data_asset_status.json")
    pipeline_health = load_json("app/static/data/pipeline_health.json")
    culture_items_latest = load_json("data/derived/culture_items_latest.json")
    culture_items_manifest = load_json("data/derived/culture_items_manifest.json")

    battle_tracks = []
    for index, track in enumerate(spotify.get("top_tracks", [])[:4], start=1):
        battle_tracks.append(
            {
                "id": f"spotify-{index}",
                "title": track.get("title", ""),
                "artist": track.get("artist", ""),
                "source": "Spotify Daily",
                "stat_label": "Rank",
                "stat_value": f"#{track.get('rank', index)}",
            }
        )

    leaderboard = []
    for index, track in enumerate(spotify.get("top_tracks", [])[:3], start=1):
        leaderboard.append(
            {
                "id": f"leader-spotify-{index}",
                "title": track.get("title", ""),
                "artist": track.get("artist", ""),
                "source": "Spotify",
                "stat_label": "Daily streams",
                "stat_value": compact_value(track.get("daily_streams", 0)),
            }
        )
    for index, track in enumerate(deezer.get("top_tracks", [])[:2], start=1):
        leaderboard.append(
            {
                "id": f"leader-deezer-{index}",
                "title": track.get("title", ""),
                "artist": track.get("artist", ""),
                "source": "Deezer",
                "stat_label": "Chart spot",
                "stat_value": f"#{track.get('position', index)}",
            }
        )

    return {
        "generated_at": culture_items_latest.get("generated_at", ""),
        "source_files": {
            "cultural_insights": "app/static/data/cultural_insights.json",
            "culture_rss": "app/static/data/culture_rss.json",
            "identity_tags": "app/static/data/identity_tags.json",
            "identity_context_feed": "app/static/data/identity_context_feed.json",
            "signal_insights": "app/static/data/signal_insights.json",
            "cta_momentum": "app/static/data/cta_momentum.json",
            "promo": "app/static/data/promo.json",
            "lead_summary": "app/static/data/lead_summary.json",
            "data_asset_status": "app/static/data/data_asset_status.json",
            "pipeline_health": "app/static/data/pipeline_health.json",
            "culture_items_latest": "data/derived/culture_items_latest.json",
            "culture_items_manifest": "data/derived/culture_items_manifest.json",
        },
        "hero": {
            "eyebrow": "World Cup Arcade",
            "title": "Pick fast,\nkeep the streak alive.",
            "summary": (
                "모바일에서는 월드컵이 메인입니다. "
                f"{promo.get('hero', {}).get('subtext', '')}"
            ).strip(),
            "updated_at": promo.get("updated_at", ""),
            "metrics": [
                {
                    "label": "battle pool",
                    "value": len(battle_tracks),
                },
                {
                    "label": "spotify leaders",
                    "value": len(spotify.get("top_tracks", [])[:6]),
                },
                {
                    "label": "deezer picks",
                    "value": len(deezer.get("top_tracks", [])[:6]),
                },
                {
                    "label": "brand leads",
                    "value": lead_summary.get("total_leads", 0),
                },
            ],
            "primary_cta": {
                "label": "PLAY NOW",
                "link": "/worldcup",
            },
            "secondary_cta": {
                "label": "OPEN FULL BOARD",
                "link": "/worldcup",
            },
        },
        "worldcup": {
            "eyebrow": "Main Feature",
            "title": "One-tap battles built like a mini game.",
            "summary": (
                "Spotify, Deezer, Billboard 신호를 바로 대결 카드로 묶었습니다. "
                "앱에서는 다음 페어가 끊기지 않게 빠르게 이어집니다."
            ),
            "metrics": [
                {"label": "spotify", "value": len(spotify.get("top_tracks", [])[:6])},
                {"label": "deezer", "value": len(deezer.get("top_tracks", [])[:6])},
                {"label": "billboard", "value": len(billboard.get("top_tracks", [])[:5])},
                {"label": "7d leads", "value": lead_summary.get("recent_seven_days", 0)},
            ],
            "battle_tracks": battle_tracks,
            "leaderboard": leaderboard,
            "primary_cta": {"label": "Play full world cup", "link": "/worldcup"},
            "secondary_cta": {"label": "Add more tracks", "link": "/playlists"},
        },
        "culture_pulse": {
            "headline": cultural_insights.get("headline", "Culture pulse"),
            "summary": culture_rss.get("summary_line", ""),
            "stories": [
                {
                    "source": story.get("source", ""),
                    "title": story.get("title", ""),
                    "summary": story.get("summary", ""),
                    "published_at": next(
                        (
                            entry.get("published", "")
                            for source in culture_rss.get("sources", [])
                            for entry in source.get("entries", [])
                            if entry.get("title") == story.get("title")
                        ),
                        "",
                    ),
                }
                for story in cultural_insights.get("stories", [])[:3]
            ],
            "chart_highlights": cultural_insights.get("chart_highlights", [])[:3],
            "normalized_items": [
                {
                    "title": item.get("title", ""),
                    "creator": item.get("creator", ""),
                    "source_type": item.get("source_type", ""),
                    "published_at": item.get("published_at", ""),
                }
                for item in culture_items_latest.get("items", [])[:4]
            ],
        },
        "identity": {
            "headline": identity_context.get("headline", signal_insights.get("hero_line", "")),
            "summary": identity_context.get("summary", identity_tags.get("notes", "")),
            "top_tags": identity_context.get("top_tags", identity_tags.get("tags", []))[:6],
            "contexts": identity_context.get("contexts", [])[:6],
            "signal_cta": signal_insights.get("cta", {"label": "Share signal", "link": "/brand-studio"}),
        },
        "monetization": {
            "context_line": cta_momentum.get("context_line", ""),
            "lead_summary": {
                "total_leads": lead_summary.get("total_leads", 0),
                "recent_seven_days": lead_summary.get("recent_seven_days", 0),
                "goal_keywords": lead_summary.get("goal_keywords", []),
            },
            "offers": [
                {
                    "tagline": offer.get("tagline", ""),
                    "title": offer.get("title", ""),
                    "description": offer.get("description", ""),
                    "price": offer.get("price", ""),
                    "bullets": offer.get("bullets", []),
                    "cta_label": offer.get("cta", {}).get("label", "Open"),
                }
                for offer in promo.get("offers", [])
            ],
            "momentum_entries": [
                {
                    "tag": entry.get("tag", ""),
                    "intent_label": entry.get("intent_label", ""),
                    "message": entry.get("message", ""),
                    "cta_label": entry.get("cta", {}).get("label", ""),
                }
                for entry in cta_momentum.get("entries", [])[:3]
            ],
        },
        "data_assets": {
            "pipeline": {
                "fresh_ratio": pipeline_health.get("fresh_ratio", 0),
                "fresh_assets": pipeline_health.get("fresh_assets", 0),
                "stale_assets": pipeline_health.get("stale_assets", 0),
                "oldest_asset_name": pipeline_health.get("oldest_asset", {}).get("name", ""),
            },
            "manifest": {
                "count": culture_items_manifest.get("count", 0),
                "schema_version": culture_items_manifest.get("schema_version", ""),
                "target_table_hint": culture_items_manifest.get("target_table_hint", ""),
                "normalized_path": culture_items_manifest.get("normalized_path", ""),
            },
            "assets": data_asset_status.get("assets", [])[:6],
        },
    }


def main() -> None:
    payload = build_payload()
    MOBILE_PAYLOAD_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MOBILE_PAYLOAD_PATH.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
