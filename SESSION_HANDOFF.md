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
- `scripts/compile_identity_tags.py`가 RSS 타이틀/요약에서 정체성 키워드·컨텍스트를 집계해 `app/static/data/identity_tags.json`에 저장하며, 랜딩의 새 Identity Tags 블록이 브랜드 문의/다이어리 CTA 앞에서 Jun의 문화 DNA를 다시 한번 강조합니다.
- Signal Intelligence 블록이 `scripts/compile_signal_insights.py`와 `app/static/data/signal_insights.json`을 바탕으로 identity 태그와 growth 키워드를 통합해 제안 CTA 앞에 Jun의 정체성과 수익화 리드를 동시에 노출합니다.

## Automation currently configured
- Daily 9 AM report job exists.
- Hourly autonomous improvement job exists.
- Both should think in terms of revenue + traffic + identity.
- No automatic deploy.

## Operating rules for future sessions
- Read `WORKLOG.md` first.
- Append to `WORKLOG.md` after every meaningful task.
- Keep changes small, commercial, and reversible.
- If blocked or risky, write the blocker in `WORKLOG.md` and propose the safest next step.

## Next recommended tasks
1. Connect external culture data sources (YouTube / Spotify / RSS)
2. Improve homepage conversion path for membership / brand inquiry
3. Add clearer identity-rich storytelling blocks
4. Strengthen trust/security presentation without hurting conversion
5. Hook the growth summary script into the hourly autonomous job so Lead Pulse numbers stay fresh
6. Run `scripts/update_billboard_hot100.py` on the autonomous job schedule so the Billboard block always reflects a recent global snapshot
7. Hook `scripts/update_deezer_chart.py` into the hourly autonomous job so the Deezer Pulse stays current.
8. Hook `scripts/update_culture_rss.py` into the hourly autonomous job so the Cultural Notes data and CTA messaging stay synchronized with fresh NYTimes/NPR/Rolling Stone signals.
9. Run `scripts/compile_identity_tags.py` inside the autonomous job as well so the Identity Tags block stays aligned with the latest RSS signals and can feed brand/membership pitches.
10. Add `scripts/compile_signal_insights.py` to the hourly autonomous job so the new Signal Intelligence block stays in sync with identity+lead data and keeps the CTA flow fresh.
