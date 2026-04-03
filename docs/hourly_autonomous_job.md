# Hourly Autonomous Pipeline

This project now batches every revenue/identity signal update into a single script so the landing page, data assets, and CRM prompts all stay synchronized once an hour.

## What it runs (in order)
1. `scripts/update_growth_summary.py` – refreshes the Lead Pulse snapshot.
2. `scripts/update_promo.py` – builds the hero/offers copy that already ran on its own before; now it rides with the rest of the pipeline.
3. `scripts/update_billboard_hot100.py`
4. `scripts/update_deezer_chart.py`
5. `scripts/update_culture_rss.py`
6. `scripts/compile_identity_tags.py`
7. `scripts/compile_identity_context_feed.py`
8. `scripts/update_guardian_music.py`
9. `scripts/compile_signal_insights.py`
10. `scripts/compile_cta_momentum.py`
11. `scripts/update_cultural_insights.py`
12. `scripts/build_culture_items.py`
13. `scripts/log_data_asset_status.py`

Each step logs its own output and the orchestrator prints a summary with durations/failure status and exits non-zero if any of the scripts fail. That makes it easy to monitor `/tmp/off-community-hourly.log` from the host Cron job.

## Scheduling
Install the following Cron entry (or let the autonomous engine call it) to keep everything fresh every hour:

```
0 * * * * cd /Users/junkim/Projects/off_community && /usr/bin/env python3 scripts/hourly_autonomous_job.py >> /tmp/off-community-hourly.log 2>&1
```

If you already had individual cron jobs for the promo or culture feeds, you can retire them once this orchestrator is live.

## Monitoring & next steps
- Inspect `/tmp/off-community-hourly.log` for failures or slow steps.
- Use the `DATA_ASSET_STATUS` card on the landing page to confirm timestamps refresh after each run.
- If you later expand the pipeline (Spotify feeds, Supabase imports, etc.), add the new scripts to `scripts/hourly_autonomous_job.py` and keep the list in sync with this document.
