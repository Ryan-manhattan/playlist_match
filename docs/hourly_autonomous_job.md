# Hourly Autonomous Pipeline

This project now batches every revenue/identity signal update into a single script so the landing page, data assets, and CRM prompts all stay synchronized once an hour.

## What it runs (in order)
1. `scripts/update_growth_summary.py` – refreshes the Lead Pulse snapshot.
2. `scripts/update_lead_source_spread.py` – re-aggregates `app/static/data/lead_summary.json` into `app/static/data/lead_source_spread.json` so the landing’s Lead Source Spotlight card can show the freshest referral mix alongside the Lead Pulse metrics.
3. `scripts/update_promo.py` – builds the hero/offers copy that already ran on its own before; now it rides with the rest of the pipeline.
4. `scripts/update_billboard_hot100.py`
5. `scripts/update_deezer_chart.py`
6. `scripts/update_spotify_kworb.py` – Kworb의 Global Daily Spotify 차트를 스냅샷으로 남기고 landing의 음악 레이더를 강화합니다.
7. `scripts/update_culture_rss.py`
8. `scripts/update_pitchfork_rss.py` – captures Pitchfork News so Jun의 브랜드/멤버십 내러티브가 글로벌 음악 커버리지를 더 빠르게 반영합니다.
9. `scripts/compile_identity_tags.py`
10. `scripts/compile_identity_context_feed.py`
11. `scripts/update_guardian_music.py`
12. `scripts/compile_signal_insights.py`
13. `scripts/compile_cta_momentum.py`
14. `scripts/update_cultural_insights.py`
15. `scripts/build_culture_items.py`
16. `scripts/import_culture_items_supabase.py` – upserts the normalized dataset into the `culture_items` table so the long-term proprietary snapshot lives beside the landing payloads.
17. `scripts/log_data_asset_status.py`

Once the summary and duration lines are printed, the orchestrator runs `scripts/collect_automation_log.py` as a lightweight post-run hook so `/tmp/off-community-hourly.log` is read after the pipeline summary actually exists. That keeps `app/static/data/automation_log.json` aligned with the very last run, letting the landing page surface the LaunchAgent success/failure message and timeline without lag.

Each step logs its own output and the orchestrator prints a summary with durations/failure status and exits non-zero if any of the scripts fail. That makes it easy to monitor `/tmp/off-community-hourly.log` from the host Cron job.

## Scheduling
### Preferred (macOS LaunchAgent)
Create a LaunchAgent so the orchestrator runs every hour without touching `/var/at/tabs`, which was previously blocked by spool/permission checks:

```
~/Library/LaunchAgents/com.offcommunity.hourly.plist
```

The plist should point at `/usr/bin/env python3 scripts/hourly_autonomous_job.py`, set the working directory to `/Users/junkim/Projects/off_community`, stream both stdout/stderr to `/tmp/off-community-hourly.log`, and use `StartInterval` 3600 plus `RunAtLoad` so updates happen immediately and every hour after. Load it with:

```
launchctl unload ~/Library/LaunchAgents/com.offcommunity.hourly.plist >/dev/null 2>&1 || true
launchctl load -w ~/Library/LaunchAgents/com.offcommunity.hourly.plist
```

If you need to stop the hourly run temporarily (for upgrades or debugging), unload the plist, edit the script, then reload it.

### Optional Cron fallback
If you prefer `cron` or need to deploy to a different host, the existing entry still works as long as the run user can write to `/var/at/tabs`:

```
0 * * * * cd /Users/junkim/Projects/off_community && /usr/bin/env python3 scripts/hourly_autonomous_job.py >> /tmp/off-community-hourly.log 2>&1
```

Retire any standalone promo/culture cron jobs once the orchestrator is live.

## Monitoring & next steps
- Inspect `/tmp/off-community-hourly.log` for failures or slow steps.
- Check `app/static/data/automation_log.json` (and the new Pipeline Health log callout) so the landing page can quote the LaunchAgent status alongside the data asset summary.
- Use the `DATA_ASSET_STATUS` card on the landing page to confirm timestamps refresh after each run.
- Confirm the Supabase `culture_items` table reflects the latest normalized asset after each run (the new `scripts/import_culture_items_supabase.py` step handles the upsert). If you later expand the pipeline (Spotify feeds, new data exports, etc.), add the new scripts to `scripts/hourly_autonomous_job.py` and keep the list in sync with this document.
