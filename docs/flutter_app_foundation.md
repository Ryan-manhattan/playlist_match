# Flutter App Foundation

The first Flutter app lives in `apps/mobile`.

## Why this structure

- The app is local-first for now so it can ship immediately without waiting on Supabase credentials or mobile API design.
- `HomeRepository` is abstract and currently backed by `LocalHomeDataSource`, which loads a bundled JSON payload.
- The payload is generated from the same website data files already powering the current project, so the app is not inventing a separate content model.

## Current mapping

- `Culture Pulse`
  - `app/static/data/cultural_insights.json`
  - `app/static/data/culture_rss.json`
  - `data/derived/culture_items_latest.json`
- `Identity`
  - `app/static/data/identity_tags.json`
  - `app/static/data/identity_context_feed.json`
  - `app/static/data/signal_insights.json`
- `CTA / monetization`
  - `app/static/data/promo.json`
  - `app/static/data/cta_momentum.json`
  - `app/static/data/lead_summary.json`
- `Data assets / future pipeline`
  - `app/static/data/data_asset_status.json`
  - `app/static/data/pipeline_health.json`
  - `data/derived/culture_items_manifest.json`

## Generation flow

Run:

```bash
python3 scripts/build_flutter_home_payload.py
```

This writes:

```text
apps/mobile/assets/data/home_payload.json
```

## Supabase path later

The app already exposes the normalized data layer metadata:

- `target_table_hint: culture_items`
- `normalized_path: data/normalized/culture_items.jsonl`
- `schema_version: 1.0`

The intended next step is to add a `SupabaseHomeRepository` that resolves the same domain models as `MobileHomeRepository`, then swap repositories by environment or feature flag without rewriting the presentation layer.
