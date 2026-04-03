# SESSION HANDOFF

## Project
- Path: `/Users/junkim/Projects/off_community`
- Primary goal:
  1. Improve monetization / revenue potential
  2. Increase visitors and return traffic
  3. Express Jun's identity, taste, and cultural point of view clearly

## Current state
- Landing page has promo-driven commercialization sections.
- Culture Pulse section was added and reads from `app/static/data/culture.json`.
- `scripts/update_promo.py` creates promo content.
- `scripts/culture_data.py` creates internal cultural snapshots.
- Pretext-based layout improvements were added to charts/worldcup UI.
- Added `scripts/update_growth_summary.py` + `app/static/data/lead_summary.json` so the landing page can show lead counts, keywords, and source signals in the new Lead Pulse card.
- Billboard Hot 100 snapshot data now lives in `app/static/data/billboard_hot100.json` and is surfaced via a new landing block; `scripts/update_billboard_hot100.py` pulls it from Billboard via requests/BeautifulSoup.
- Deezer Global Pulse JSON (`app/static/data/deezer_chart.json`) and `scripts/update_deezer_chart.py` now feed a new landing block so Jun의 글로벌 차트 감성이 실시간으로 기록됩니다.
- “Cultural Notes” 섹션과 `app/static/data/culture_rss.json`을 추가하여 NYTimes Arts/NPR Music/Rolling Stone RSS 스냅샷이 브랜드·다이어리 CTA 앞에서 Jun의 취향을 보여주도록 했습니다 (`scripts/update_culture_rss.py`).
- `scripts/update_pitchfork_rss.py`가 Pitchfork News 피드를 `app/static/data/pitchfork_rss.json`에 기록하고 랜딩의 Pitchfork Signal 블록에 글로벌 커버리지를 직결시켜 Jun의 브랜드/멤버십 내러티브를 강화합니다.
- `scripts/compile_identity_tags.py`가 RSS 타이틀/요약에서 정체성 키워드·컨텍스트를 집계해 `app/static/data/identity_tags.json`에 저장하며, 랜딩의 새 Identity Tags 블록이 브랜드 문의/다이어리 CTA 앞에서 Jun의 문화 DNA를 다시 한번 강조합니다.
- Signal Intelligence 블록이 `scripts/compile_signal_insights.py`와 `app/static/data/signal_insights.json`을 바탕으로 identity 태그와 growth 키워드를 통합해 제안 CTA 앞에 Jun의 정체성과 수익화 리드를 동시에 노출합니다.
- CTA Momentum 블록과 `scripts/compile_cta_momentum.py`를 통해 identity/lead/날씨 컨텍스트를 `app/static/data/cta_momentum.json`으로 정형화하고 Jun의 문화 감성과 수익화 리드를 CTA copy로 바로 보여줍니다.
- `scripts/update_cultural_insights.py`가 RSS + Billboard + Deezer 데이터를 합쳐 `app/static/data/cultural_insights.json`을 만들고, 랜딩에 Cultural Insight Brief 섹션을 추가해 브랜드 CTA 앞에서 핵심 키워드/스토리/차트 포인트를 보여줍니다.
- `scripts/log_data_asset_status.py`와 `app/static/data/data_asset_status.json`이 문화/리드/CTA 자산의 타임스탬프와 메트릭을 정리하고, 랜딩의 Data Asset Inventory 카드로 어떤 데이터 기반으로 수익화 흐름이 만들어지는지 투명하게 설명합니다.
- `scripts/compile_identity_context_feed.py`가 identity_tags 컨텍스트를 `app/static/data/identity_context_feed.json`으로 정리하고, 랜딩에 Identity Context Feed 섹션을 추가해 CTA 직전에 Jun의 정체성과 문화 맥락을 다시 보여줍니다.
- Guardian Music Radar 블록이 `scripts/update_guardian_music.py`와 `app/static/data/guardian_music_feed.json`를 이용해 Guardian music 기사 타이틀·요약·발행 시점을 기록하고, Jun의 브랜드/멤버십 CTA 앞뒤에 외부 문화 신호를 덧씌웁니다.
- `scripts/update_spotify_kworb.py`가 Kworb Global Daily Spotify 차트를 `app/static/data/spotify_daily_chart.json`에 기록하고 있으며, 런딩의 Spotify Radar 블록과 데이터 자산 카드가 이 스냅샷을 추적합니다.
- `scripts/build_culture_items.py`가 culture / RSS / Billboard / Deezer 데이터를 공통 스키마로 정규화해 `data/normalized/culture_items.jsonl`과 `data/derived/culture_items_manifest.json`을 생성하므로, 나중에 Supabase `culture_items` 테이블로 이관하기 쉬운 로컬 데이터 레이어가 생겼습니다.
- `scripts/import_culture_items_supabase.py`가 정규화 JSONL을 Supabase `culture_items` 테이블에 upsert해 시간당 파이프라인만큼 Postgres에 장기 기록을 남기기 시작했습니다.
- `scripts/hourly_autonomous_job.py` now calls `datetime.now(tz=timezone.utc)` for log timestamps, `scripts/import_culture_items_supabase.py` prepends the repo root to `sys.path`, and `utils/app_settings.py` tolerates a missing `python-dotenv`; running `/usr/bin/env python3 scripts/hourly_autonomous_job.py >> /tmp/off-community-hourly.log 2>&1` refreshed the JSON assets and left `/tmp/off-community-hourly.log` ending with a success summary even though the Supabase client/credentials are still absent (that step now just logs a skip).

- `scripts/pipeline_health.py`가 `data_asset_status.json`을 분석해 freshness/staleness 지표를 `app/static/data/pipeline_health.json`에 기록하며, `scripts/hourly_autonomous_job.py`가 새 스크립트를 호출하고 랜딩의 Pipeline Health 카드가 자동화 상태/CTA 앞에서 보이게 되었습니다.
- `scripts/collect_automation_log.py`가 `/tmp/off-community-hourly.log`를 읽어 `app/static/data/automation_log.json`을 만들고 있으며, 홈 페이지의 Pipeline Health callout과 `automation_log` asset이 LaunchAgent가 실제로 완주했는지 빠르게 보증할 수 있도록 돕고 있습니다.


## Automation currently configured
- Daily 9 AM report job exists.
- Hourly autonomous improvement job now runs `scripts/hourly_autonomous_job.py`, which courts the promo, chart, RSS (now including Pitchfork), identity, CTA, Guardian, Spotify, and data asset scripts in one sweep. The new `com.offcommunity.hourly` LaunchAgent runs the orchestrator every 3600 seconds, logs to `/tmp/off-community-hourly.log`, and is described in `docs/hourly_autonomous_job.md`, so the full pipeline stays synchronized without hitting the old Cron spool block.
- I manually executed the LaunchAgent command (`/usr/bin/env python3 scripts/hourly_autonomous_job.py >> /tmp/off-community-hourly.log 2>&1`) and saw the log end with "All steps completed successfully" while `app/static/data/data_asset_status.json` got a fresh timestamp, so the scheduled job should now keep the data assets aligned.
- `docs/hourly_autonomous_job.md` still documents the Cron snippet as an optional fallback, but it only works when the host user can write to `/var/at/tabs`, so prefer the LaunchAgent on macOS.
- Both should think in terms of revenue + traffic + identity.
- No automatic deploy.

## Next recommended tasks
1. After the next scheduled LaunchAgent run, check `/tmp/off-community-hourly.log` again so it still ends with "All steps completed successfully" and verify `app/static/data/data_asset_status.json` shares the same timestamp as the Data Asset Inventory card, proving the automated run kept the assets fresh.
2. Provide Supabase credentials plus the `supabase` library so `scripts/import_culture_items_supabase.py` can upsert into the `culture_items` table again; rerun the hourly pipeline afterwards to confirm Supabase reflects the latest normalized snapshot.
3. Continue sourcing new cultural signals (YouTube dips, Spotify spikes, additional RSS beyond Pitchfork/NME) and, when ready, integrate the new worker scripts into `scripts/hourly_autonomous_job.py` so Jun's identity narrative keeps ahead of trends.

4. After the next automation sweep, revisit the new Pipeline Health card and `app/static/data/pipeline_health.json` to confirm the fresh/stale counters reset; if stale assets accumulate, log a follow-up fix (e.g., add alerts or stronger retries).


## Operating rules for future sessions
- Read `WORKLOG.md` first.
- Append to `WORKLOG.md` after every meaningful task.
- Keep changes small, commercial, and reversible.
- If blocked or risky, write the blocker in `WORKLOG.md` and propose the safest next step.

