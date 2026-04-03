# off_community mobile

This package is the first Flutter app foundation for the project. It currently ships a single home experience built from a generated local asset:

- `assets/data/home_payload.json`

That payload is produced from the existing website data layer with:

```bash
python3 scripts/build_flutter_home_payload.py
```

Current source files:

- `app/static/data/cultural_insights.json`
- `app/static/data/culture_rss.json`
- `app/static/data/identity_tags.json`
- `app/static/data/identity_context_feed.json`
- `app/static/data/signal_insights.json`
- `app/static/data/cta_momentum.json`
- `app/static/data/promo.json`
- `app/static/data/lead_summary.json`
- `app/static/data/data_asset_status.json`
- `app/static/data/pipeline_health.json`
- `data/derived/culture_items_latest.json`
- `data/derived/culture_items_manifest.json`

Architecture notes:

- `HomeRepository` is intentionally abstract so a future Supabase-backed repository can replace the local asset without changing the UI.
- The bundled payload already carries `target_table_hint: culture_items` and normalized item metadata so the app aligns with the existing data generation pipeline.
- Platform folders were not generated in this session because the sandbox blocks the Homebrew-managed `flutter` wrapper from updating its SDK cache. Once that restriction is removed, run `flutter create .` inside `apps/mobile` to add `android/`, `ios/`, and other platform shells around the existing app code.
