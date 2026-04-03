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


def build_payload() -> dict[str, Any]:
    cultural_insights = load_json("app/static/data/cultural_insights.json")
    culture_rss = load_json("app/static/data/culture_rss.json")
    identity_tags = load_json("app/static/data/identity_tags.json")
    identity_context = load_json("app/static/data/identity_context_feed.json")
    signal_insights = load_json("app/static/data/signal_insights.json")
    cta_momentum = load_json("app/static/data/cta_momentum.json")
    promo = load_json("app/static/data/promo.json")
    lead_summary = load_json("app/static/data/lead_summary.json")
    data_asset_status = load_json("app/static/data/data_asset_status.json")
    pipeline_health = load_json("app/static/data/pipeline_health.json")
    culture_items_latest = load_json("data/derived/culture_items_latest.json")
    culture_items_manifest = load_json("data/derived/culture_items_manifest.json")

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
            "eyebrow": "Jun taste system",
            "title": "Culture-first community,\nshaped for an app-native future.",
            "summary": (
                f"{cultural_insights.get('headline', '')} "
                f"{promo.get('hero', {}).get('subtext', '')}"
            ).strip(),
            "updated_at": promo.get("updated_at", ""),
            "metrics": [
                {
                    "label": "culture items",
                    "value": culture_items_manifest.get("count", 0),
                },
                {
                    "label": "fresh ratio",
                    "value": f"{pipeline_health.get('fresh_ratio', 0)}%",
                },
                {
                    "label": "offers",
                    "value": len(promo.get("offers", [])),
                },
                {
                    "label": "leads",
                    "value": lead_summary.get("total_leads", 0),
                },
            ],
            "primary_cta": {
                "label": promo.get("hero", {}).get("ctas", [{}])[0].get("text", "Explore"),
                "link": promo.get("hero", {}).get("ctas", [{}])[0].get("link", "/"),
            },
            "secondary_cta": {
                "label": promo.get("hero", {}).get("ctas", [{}, {}])[1].get("text", "View Studio"),
                "link": promo.get("hero", {}).get("ctas", [{}, {}])[1].get("link", "/brand-studio"),
            },
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
