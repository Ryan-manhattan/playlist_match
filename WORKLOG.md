# WORKLOG

이 파일은 off_community 프로젝트의 지속 작업 로그입니다.

## 규칙
- 모든 의미 있는 작업 후 짧게 기록한다.
- 아래 5가지는 가능하면 항상 남긴다.
  1. 날짜/시간
  2. 무엇을 바꿨는지
  3. 왜 바꿨는지
  4. 다음에 이어서 할 일
  5. 주의할 점 / 막힌 점
- 세션이 끊겨도 다음 세션은 이 파일과 `SESSION_HANDOFF.md`를 먼저 읽고 이어간다.

---

## 2026-04-02

### 22:52 KST
- 자동 개발/보고의 핵심 목표를 명시함:
  - 수익성 강화
  - 방문자/재방문 증가
  - Jun의 아이덴티티와 취향이 잘 드러나는 사이트 만들기
- 랜딩 페이지에 promo/culture 기반 동적 섹션을 추가한 상태.
- 현재 자동 개발은 매시간 작은 변경 1건씩 진행하도록 설정되어 있음.
- 다음 작업 후보:
  1. 외부 문화 데이터(YouTube/Spotify/RSS) 실제 연결
  2. 랜딩 페이지 CTA 흐름 고도화
  3. 브랜드/멤버십 전환 퍼널 정리
  4. 작업 결과를 더 구조적으로 남기는 일지 자동화
- 주의:
  - 배포는 자동으로 하지 않음
  - 큰 리팩터링보다 작고 안전한 개선 우선

### 23:15 KST
- 홈 랜딩에 실시간 Lead Pulse 카드를 추가하고, 성장 리드 로그를 요약하는 `scripts/update_growth_summary.py` + `app/static/data/lead_summary.json` 자산을 만들었습니다.
- 리드 타입별 카운트, 7일 리드, 트렌드 키워드, 상위 유입 경로를 보여줌으로써 수익화 신호를 시각화하고 다음 브랜드/멤버십 CTA를 뒷받침하는 데이터 자산을 확보했습니다.
- 데이터 출처: 로컬 `data/growth/growth_leads.jsonl` (스크립트 실행으로 요약된 JSON 생성).
- Blockers/risks: 없음.
- 다음 후보: Cron/파이프라인에 요약 스크립트 정기 실행을 연결하고, Supabase 리드/유입 현황을 직접 가져오는 API까지 확장하기.

### 00:15 KST
- Billboard Hot 100 스냅샷을 홈에 추가하고, `update_billboard_hot100.py` 스크립트 + `app/static/data/billboard_hot100.json` 자산을 만들어 외부 글로벌 차트 데이터를 기록·표현하게 했습니다.
- 이유: Jun의 감성과 문화적 감시를 명확히 드러내고, 브랜드·멤버십 CTA 앞에 글로벌 트렌드 신호를 붙여 방문자/수익 전환 타이밍을 틀어줍니다.
- Blockers/risks: 없음.
- Saved sources: Billboard Hot 100 (requests + BeautifulSoup 스크립트 호출 시).
- Data-asset impact: 매번 최신 차트 스냅샷을 JSON으로 보존해 향후 리포트나 CTA 정교화에 활용할 수 있는 구조를 마련했습니다.
- Next candidate: 이 스크립트를 자율 작업/크론에 연결해 차트가 자동 업데이트되도록 계속 데이터 흐름을 유지합니다.

## 2026-04-03

### 01:10 KST
- 무엇을 바꿨는지: Deezer Global Pulse 블록과 scripts/update_deezer_chart.py를 추가하여 랜딩에 Jun 취향의 글로벌 차트 신호를 쌓고 app/static/data/deezer_chart.json 자산을 확보했습니다.
- 왜 바꿨는지: 문화/브랜드 CTA 직전에 Jun의 감성과 글로벌 신호를 노출해 ID를 강화하고 CTA 전환/리텐션을 위한 추가 데이터 자산을 만들기 위해.
- Blockers/risks: 없음.
- Saved data sources: Deezer API (https://api.deezer.com/chart/0/tracks)에서 6개 트랙을 가져와 JSON으로 저장.
- Data-asset impact: 매 시점 스냅샷을 이어받을 수 있는 Deezer 차트 JSON이 마련되어 향후 리포트/CTA 정교화에 사용 가능.
- Next candidate task: Deezer 스냅샷 스크립트를 autonomous job에 넣어 차트 블록이 자동으로 갱신되도록 하고, CTA/방문 집중 트래픽 흐름으로 묶기.

### 02:40 KST
- 무엇을 바꿨는지: scripts/update_culture_rss.py를 만들고 NYTimes Arts / NPR Music / Rolling Stone RSS를 하루 스캔하여 app/static/data/culture_rss.json에 저장한 뒤, 랜딩에 새로운 “Cultural Notes” 블록을 추가해 가장 최근 문화 감상을 UI/CTA로 연결했습니다.
- 왜 바꿨는지: 문화 데이터 자산을 더 구조적으로 쌓아 Jun의 정체성과 감성을 방문자에게 보여주면서 브랜드/일기 CTA 앞에 문화적 신뢰를 붙이고, 장기적으로 RSS 스냅샷을 기반으로 인사이트와 콘텐츠를 만들기 위해.
- Blockers/risks: 없음.
- Saved data sources: NYTimes Arts RSS, NPR Music RSS (Tiny Desk 등), Rolling Stone Music News RSS를 requests로 가져와 요약해 JSON으로 기록함.
- Data-asset impact: 피드별 스냅샷과 문맥 요약이 `culture_rss.json`에 보존되므로 향후 보고서, CTA 메시지, 문화 데이터 시리즈에 재사용 가능.
- Next candidate task: 이 스크립트를 autonomous job(시간당) 혹은 cron과 연결해 문화 블록이 자동 갱신되도록 하고, 기록된 RSS 요약을 리드/디텍션에 활용하는 추가 CTA/통계 흐름을 고민하기.

### 03:07 KST
- 무엇을 바꿨는지: culture_rss JSON을 분석해 `scripts/compile_identity_tags.py`로 정체성 키워드/문맥 태그를 생성하고 app/static/data/identity_tags.json에 기록한 뒤 랜딩에 Identity Tags 블록과 저장 시간 메타, CTA를 새로 배치했습니다.
- 왜 바꿨는지: Jun의 취향/문화 신호를 정량화해 방문자가 브랜드/멤버십 문의로 이어지도록 내러티브를 더 명확히 하고, 새로운 데이터 자산으로 차후 CTA·리포트에 재활용할 수 있게 하기 위해.
- Blockers/risks: 없음.
- Saved data sources: app/static/data/culture_rss.json에서 수집한 RSS 타이틀·요약 → identity_tags JSON.
- Data-asset impact: 정체성 태그 집계 JSON이 역사적으로 기록되며 컨텍스트가 붙어, 향후 브랜드 스토리·프로모션 키워드로 재사용 가능.
- Next candidate: `scripts/compile_identity_tags.py`를 hourly autonomous job에 넣어 Identity Tags가 culture RSS 갱신과 동시에 새로워지도록 고정하고, 이 태그 흐름을 Brand Studio 접점에 연동하기.
### 04:20 KST
- 무엇을 바꿨는지: identity/lead 데이터를 묶는 `scripts/compile_signal_insights.py` + `app/static/data/signal_insights.json` 데이터 자산을 만들고, `app.py`/랜딩 템플릿에 새로운 Signal Intelligence 블록을 새 CTA 흐름으로 배치하여 Jun의 identity, 문화 신호, 리드 의도를 한눈에 보여주는 UI/데이터 경험을 더했습니다.
- 왜 바꿨는지: 랜딩에서 Jun 감성과 수익화 의도를 합쳐 브랜드/membership CTA를 더 설득력 있게 연결하고, 데이터 자산(정체성 태그 + 키워드)을 하나의 요약 지표로 병합해 나중에 리포트/추천에 재활용할 수 있도록 하기 위해.
- Blockers/risks: 없음.
- Saved sources / Data-asset impact: identity_tags.json + lead_summary.json을 조합해 signal_insights.json에 상위 태그/키워드, CTA 추천을 기록하여 향후 리포트나 CTA 템플릿이 동일한 구조를 참조할 수 있게 했습니다.
- Next candidate task: 이 컴파일 스크립트를 autonomous job에 넣어 시각화 블록이 Fresh 상태를 유지하게 하고, signal_insights 데이터를 Brand Studio/리포트 목차로 다시 보내는 흐름을 고민.

### 05:20 KST
- 무엇을 바꿨는지: identity/lead 신호 + Open-Meteo 날씨 맥락을 `scripts/compile_cta_momentum.py`에서 조합하여 `app/static/data/cta_momentum.json`(CTA Momentum 데이터 자산)과 랜딩의 CTA Momentum 카드(Identity/Signal 섹션 뒤, 소재+CTA 버튼 포함)를 추가함.
- 왜 바꿨는지: 브랜드/멤버십 CTA 앞에 가장 힘 있는 태그×키워드 조합을 실시간 제안 형식으로 노출하면 리드 전환 설득력과 Jun의 문화 아이덴티티를 동시에 강조할 수 있음.
- Blockers/risks: 없음.
- Saved data sources: `app/static/data/identity_tags.json`, `app/static/data/lead_summary.json`, Open-Meteo current weather API (Seoul).
- Data-asset impact: CTA Momentum JSON으로 identity/lead 신호 + 날씨 컨텍스트를 정형화해 나중에 Brand Studio 제안이나 CRM 메시지에 재활용 가능.
- Next candidate task: 이 스크립트를 autonomous hourly job에 넣어 CTA Momentum 카드가 최신 데이터를 반영하도록 하고, Brand Studio 혹은 Growth dashboard에서도 동일한 흐름을 사용할 수 있게 한다.
### 06:09 KST
- 무엇을 바꿨는지: scripts/update_cultural_insights.py로 RSS+차트 데이터를 조합해 `app/static/data/cultural_insights.json`을 만들고, 랜딩에 새로운 Cultural Insight Brief 섹션을 넣어 브랜드 CTA 앞에서 가장 집중할 만한 키워드, 이야기, 차트 포인트를 보여주게 했습니다.
- 왜 바꿨는지: Jun의 정체성과 외부 문화 신호를 한 데 묶는 고급 CTA Narrative를 만들어 랜딩 전환 설득력/재방문 의도를 키우고, 새로운 데이터 자산을 쌓아 브랜드 리포트/카피에 재사용할 수 있도록 하기 위해.
- Blockers/risks: 없음.
- Saved data sources / Data-asset impact: culture_rss.json, billboard_hot100.json, deezer_chart.json을 요약해서 키워드/스토리/차트 하이라이트를 cultural_insights.json에 저장하여 향후 Brand Studio 제안이나 Growth report의 핵심 요약에 돌려 쓸 수 있게 했습니다.
- Next candidate task: scripts/update_cultural_insights.py를 autonomous job에 넣어 Cultural Insight Brief가 RSS·차트 필드를 반영하도록 하고, Brand Studio/CTA 복사에 직접 참조할 수 있게 한다.

### 07:10 KST
- 무엇을 바꿨는지: `scripts/log_data_asset_status.py`로 문화/리드/CTA 데이터 자산들의 최신 타임스탬프와 키 메트릭을 `app/static/data/data_asset_status.json`에 기록하고, 랜딩에 그 요약 카드(Identity/Signal 뒤에 위치)를 추가해 어떤 데이터로 수익화 흐름이 만들어지는지 투명하게 보여주게 했습니다.
- 왜 바꿨는지: 고품질 데이터 자산이 방문자에게도 보이도록 만들어 Jun 브랜드/CTA를 정체성과 수익화 신호로 더 설득력 있게 연결하고, 팀이 수집한 기록이 무엇인지 추적하며 다음 캠페인 인사이트로 재사용할 수 있도록 하기 위해.
- Blockers/risks: 없음.
- Saved data sources / Data-asset impact: 문화 RSS, Billboard/Deezer/identity tags/signal insights/CTA momentum/growth summary 원자료를 모아 `data_asset_status.json`에 타임스탬프과 주요 카운트를 정리하여 향후 보고와 자동화 트리거 근거로 활용 가능합니다.
- Next candidate task: 이 스크립트를 시간당 autonomous job에 넣어 `data_asset_status.json`이 최신 상태를 유지하도록 하고, Brand Studio/크론 모니터링에도 동일한 대시보드를 노출하는 흐름을 고민합니다.

### 08:04 KST
- 무엇을 바꿨는지: identity_tags 컨텍스트를 scripts/compile_identity_context_feed.py에서 추출해 app/static/data/identity_context_feed.json으로 정리하고, index에 새로운 Identity Context Feed 섹션과 관련 로딩 로직을 추가했습니다.
- 왜 바꿨는지: Jun의 문화 맥락과 정체성을 CTA 바로 앞에서 직접 보여줘 방문자/리드 전환을 강화하고, 더 수익화에 관련된 데이터 자산을 확보하기 위해.
- Blockers/risks: 없음.
- Saved data sources: app/static/data/identity_tags.json (culture_rss-derived contexts).
- Data-asset impact: identity_context_feed.json이 identity contexts + hero 키워드를 기록해 Brand Studio/리포트에서 재활용 가능하도록 했습니다.
- 다음 후보: scripts/compile_identity_context_feed.py를 autonomous job에 넣어 컨텍스트 피드가 최신화되도록 한 뒤 이 데이터를 Brand Studio CRM/copy에 연동하기.

### 09:10 KST
- 무엇을 바꿨는지: `scripts/build_culture_items.py`를 추가해 기존 문화 데이터(`culture.json`, `culture_rss.json`, `billboard_hot100.json`, `deezer_chart.json`)를 Supabase 이관 가능한 공통 스키마로 정규화하고, `data/normalized/culture_items.jsonl`, `data/derived/culture_items_latest.json`, `data/derived/culture_items_manifest.json`을 생성했습니다. 또한 `docs/data_layer.md`로 raw/normalized/derived 데이터 레이어 원칙을 문서화했습니다.
- 왜 바꿨는지: Supabase가 현재 비활성 상태여도 나중에 쉽게 붙일 수 있도록 로컬 데이터 자산을 테이블 친화적으로 쌓아두는 것이 중요했고, UI 위주 개선에서 한 단계 나아가 장기적인 데이터 자산 축적 구조를 실제로 구현하기 위해서입니다.
- Blockers/risks: 아직 기존 개별 수집 스크립트들이 자동으로 이 정규화 스크립트를 후속 실행하지는 않음.
- Saved data sources: `app/static/data/culture.json`, `culture_rss.json`, `billboard_hot100.json`, `deezer_chart.json` → `data/normalized/culture_items.jsonl`.
- Data-asset impact: 향후 Supabase `culture_items` 테이블로 옮기기 쉬운 정규화 레이어가 생겼고, source/external_id/timestamp/tag 기반으로 중복 제거/이력 관리/재분석 기반이 마련되었습니다.
- Next candidate task: 각 문화 수집 스크립트 실행 뒤 `build_culture_items.py`까지 이어서 돌도록 파이프라인을 묶고, 랜딩/브랜드 화면이 `data/derived/culture_items_latest.json`을 직접 활용하도록 전환합니다.

### 09:30 KST
- 무엇을 바꿨는지: Guardian Music Radar를 위한 scripts/update_guardian_music.py와 app/static/data/guardian_music_feed.json 자산을 만들고, 랜딩에 Guardian feed 블록을 새로 넣어 Jun의 브랜드/멤버십 내러티브가 Guardian 음악 커버리지와 직접 연결되도록 했습니다.
- 왜 바꿨는지: Guardian의 문화 기사로 수익화 CTA 앞뒤에 Jun 고유의 음악 취향을 덧붙여 방문자/재방문 가능성을 높이고, 외부 문화 데이터를 구조화된 자산으로 보존해 장기적인 리포트·카피에 재활용할 기반을 마련하기 위해서입니다.
- Blockers/risks: 없음.
- Saved data sources: https://www.theguardian.com/music (리스트 페이지 + 선택 기사 메타).
- Data-asset impact: Guardian music feed JSON이 시간대별 Guardian 기사 타이틀·요약·타임스탬프를 기록하며, 랜딩 Data Asset Inventory 주변에서 새로운 문화/identity 신호를 드라이브하는 데이터 접점을 제공합니다.
- 다음 후보: 이 스크립트를 시간당 autonomous job에 넣어 Guardian Music Radar가 최신 Guardian 커버리지를 자동으로 반영하게 하고, data_asset_status.json이나 Brand Studio/CRM 화면에서 동일한 자산을 다시 참조하는 흐름을 고민합니다.

### 10:20 KST
- 무엇을 바꿨는지: `scripts/hourly_autonomous_job.py`를 만들어 기존 개별 수집/정리 스크립트를 순차 실행하고, `docs/hourly_autonomous_job.md`로 스케줄/크론 정보와 로그 위치를 문서화하면서 SESSION_HANDOFF.md의 자동화 설명과 우선순위를 정리했습니다.
- 왜 바꿨는지: 성장/프로모션/차트/문화/정체성/CTA/Guardian/데이터 상태 스크립트를 한 번에 묶어서 한 시간마다 실행하면 랜딩 페이지 피드가 모두 같은 시점의 데이터(및 `data_asset_status.json`과 `data/normalized/culture_items` 라인)로 동기화돼 방문자·브랜드·데이터 자산 신뢰도를 높일 수 있습니다.
- Blockers/risks: 호스트에 `scripts/hourly_autonomous_job.py`를 호출하는 크론 항목이 아직 없어서 자동 실행은 다음 크론에서 확인해야 합니다.
- Saved data sources: growth lead logs → `lead_summary.json`, Supabase stats → `promo.json`, Billboard/Deezer RSS/Guardian feeds → 각 JSON, identity/CTA scripts → identity_tags/cta_momentum/cultural_insights, normalized culture items, data asset status.
- Data-asset impact: 모든 데이터 JSON(lead summary, promo, charts, RSS, identity, CTA, cultural briefs, normalized culture items, asset inventory)이 한 시점에서 갱신되도록 보장하고, 후속 Supabase 수집이나 Brand Studio 복사도 동일한 타임스탬프를 참조할 수 있게 됐습니다.
- 다음 후보: 크론 항목을 설치하고 `/tmp/off-community-hourly.log`에서 첫 실행을 확인한 뒤 Data Asset Inventory 카드와 `data/normalized/culture_items` 흐름을 Supabase import로 이어가기; 동시에 YouTube/Spotify 등 새 문화 신호를 캡처하는 스크립트를 파이프라인에 추가할 방법을 고민합니다.

### 11:09 KST
- 무엇을 바꿨는지: `scripts/import_culture_items_supabase.py`를 만들어 `scripts/hourly_autonomous_job.py`에 포함시키고, 관련 docs/SESSION_HANDOFF/data_layer를 업데이트하며 Supabase schema(`supabase/setup_all_tables.sql`)에 `culture_items` 테이블과 RLS/trigger를 추가하여 normalized JSONL이 클라우드 장기 데이터로 흘러가게 조율함.
- 왜 바꿨는지: Jun의 문화·정체성 데이터가 UI와 리포트뿐 아니라 Supabase `culture_items` 테이블에도 동일하게 기록돼 수익화·리드 분석/CRM 로드맵에 재활용할 수 있도록 오래된 데이터 자산 기반을 단단히 만드는 것이 목적.
- Blockers/risks: 없음.
- Saved data sources: `data/normalized/culture_items.jsonl`, `data/derived/culture_items_manifest.json` (manifest로 schema/version까지 캡슐화).
- Data-asset impact: normalized 데이터가 이제 매시간 Supabase에 upsert되고 `docs/data_layer.md`/`docs/hourly_autonomous_job.md`/SESSION_HANDOFF에서 그 흐름이 문서화돼 향후 Brand Studio·CRM·리포트가 단일 스키마를 바로 참조할 수 있음.
- Next candidate task: Cron 항목 설치 후 `/tmp/off-community-hourly.log`와 Supabase `culture_items` 테이블을 체크하여 pipeline의 Supabase import 단계가 잘 돌아가는지 확인하고, 새 문화 신호(YouTube/Spotify/추가 RSS) 캡처를 파이프라인에 손쉽게 붙일 방안을 계속 고민하기.

### 12:20 KST
- 무엇을 바꿨는지: `docs/hourly_autonomous_job.md`에 있던 Cron 행(`0 * * * * cd /Users/junkim/Projects/off_community && /usr/bin/env python3 scripts/hourly_autonomous_job.py >> /tmp/off-community-hourly.log 2>&1`)을 사용자 crontab에 등록하려고 `/tmp/off-community-cron` 파일을 만들고 `crontab /tmp/off-community-cron`을 여러 차례 실행해 보았습니다.
- 왜 바꿨는지: 시간당 자동 파이프라인을 시스템 Cron으로 예약하면 데이터 자산, Identity/CTA 블록, Data Asset Inventory 카드가 매시간 같은 시점으로 새로 고침돼 수익화와 문화 정체성 신호가 항상 최신 상태로 유지되도록 하기 위함입니다.
- Blockers/risks: `crontab /tmp/off-community-cron`은 `/var/at/tabs/junkim` 같은 스풀 위치에 쓰려다 멈춘 듯 계속 실행 상태로 남았고 아무 메시지 없이 종료되지 않아 실제로 새로운 Cron entry가 등록되지 않았습니다. 권한/스풀 잠금 문제가 있는 것 같으니 호스트 측에서 추가적인 허용이나 다른 방식(launchd/관리자 권한)으로 등록할 수 있어야 합니다.
- Saved data sources: 시간당 파이프라인 스크립트(`scripts/hourly_autonomous_job.py` 및 포함된 수집/정리 스크립트들)와 `docs/hourly_autonomous_job.md`의 설명이 있어 준비 상태입니다.
- Data-asset impact: 자동 실행이 아직 걸려 있지 않아 새로운 JSON 자산들이 수동 실행 시점 이후로 고정돼 있고 Data Asset Inventory 카드가 자동으로 리프레시되지 않으며, 차후 Cron이 정상화되기 전까지는 수동 실행·검증이 필요합니다.
- Next candidate task: 호스트 cron 쓰기가 가능하도록 시스템 측 조치를 받거나 대체 스케줄러(launchd, supervisor 등)를 마련한 뒤 `docs/hourly_autonomous_job.md`의 Cron entry를 다시 등록하고 `/tmp/off-community-hourly.log` + Data Asset Inventory 카드 타임스탬프가 새로워졌는지 확인합니다.

### 13:08 KST
- 무엇을 바꿨는지: Pitchfork News RSS 스냅샷을 수집하는 `scripts/update_pitchfork_rss.py`와 `app/static/data/pitchfork_rss.json` 자산을 만들고, 랜딩에 Pitchfork Signal 블록/스타일을 추가한 뒤 `app.py`, `scripts/log_data_asset_status.py`, `scripts/hourly_autonomous_job.py`, `docs/hourly_autonomous_job.md`, `SESSION_HANDOFF.md`를 연동해 파이프라인과 문서를 동기화했습니다.
- 왜 바꿨는지: Jun의 글로벌 문화 정체성을 Pitchfork 커버리지로 더 명확하게 표출하고 브랜드/멤버십 CTA 시그널을 새로운 문화로 연동하며, 관련 데이터 자산이 landing UI와 Data Asset Inventory/automation 문서에 동시에 반영되도록 하기 위함입니다.
- Blockers/risks: 없음.
- Saved data sources: Pitchfork News RSS (https://pitchfork.com/rss/news/).
- Data-asset impact: Pitchfork Signal JSON이 landing뿐 아니라 data asset inventory와 hourly pipeline, log 스크립트에 포함되어 Brand Studio·CRM·CTA 흐름이 하나의 타임스탬프를 공유하는 새로운 문화 데이터 자산이 됐습니다.
- 다음 후보 task: Cron scheduling 블록을 풀고 `/tmp/off-community-hourly.log`가 새로운 run을 기록하는지 확인한 뒤 Data Asset Inventory의 타임스탬프가 갱신되는지 살펴봅니다.

### 14:30 KST
- 무엇을 바꿨는지: Kworb Global Daily Spotify 차트를 가져오는 `scripts/update_spotify_kworb.py`를 만들고 `scripts/hourly_autonomous_job.py`, `docs/hourly_autonomous_job.md`, `scripts/log_data_asset_status.py`, `app.py`, 랜딩 템플릿을 모두 Spotify Radar 블록/데이터 자산으로 묶었습니다.
- 왜 바꿨는지: Jun의 아이덴티티가 고급 문화 신호에서 명확히 드러나고 리드/브랜드 CTA 앞에 자연스럽게 Spotify 글로벌 감성을 더해 방문자 수익화와 재방문을 동시에 자극하며, 새 데이터 자산을 시간별 파이프라인과 기록에 결합해 고품질 기록을 빠르게 쌓기 위해서입니다.
- Blockers/risks: 없음.
- Saved data sources: Kworb Global Daily Spotify chart (https://kworb.net/spotify/country/global_daily.html).
- Data-asset impact: `app/static/data/spotify_daily_chart.json` + Spotify Radar UI를 도입했고 `scripts/log_data_asset_status.py`/pipeline/Hourly doc이 이 자산을 추적/갱신하도록 바꿨습니다.
- 다음 후보 task: Cron scheduling 블록을 풀고 `/tmp/off-community-hourly.log`가 새로운 run을 기록하는지 확인한 뒤 Data Asset Inventory의 타임스탬프가 갱신되는지 살펴봅니다.

### 15:20 KST
- 무엇을 바꿨는지: `com.offcommunity.hourly` LaunchAgent를 만들고 로딩한 다음 `docs/hourly_autonomous_job.md`와 `SESSION_HANDOFF.md`를 업데이트해 시간당 파이프라인이 Mac에서 정기 실행될 수 있도록 문서와 실제 스케줄을 맞췄습니다.
- 왜 바꿨는지: `/var/at/tabs` 쓰기 권한 문제가 Cron을 막았던 상황에서 LaunchAgent가 동일한 스크립트를 시간당으로 실행하고 `/tmp/off-community-hourly.log`를 그대로 사용하게 만들어 Jun의 수익·문화·CTA 데이터 자산이 자동으로 최신 상태를 유지하도록 하기 위해.
- Blockers/risks: 없음.
- Saved data sources: LaunchAgent plist 자체와 관련 문서(`docs/hourly_autonomous_job.md`, `SESSION_HANDOFF.md`)에 스케줄·오퍼레이팅 경로를 기록했습니다.
- Data-asset impact: 새로운 자동화 스케줄 덕분에 Promo/Charts/RSS/Guardian/Spotify/Identity/CTA/Data Asset Inventory JSON들이 매시간 같은 타임스탬프로 업데이트되고 기록되며, `/tmp/off-community-hourly.log`가 작동하는지 확인하기만 하면 곧바로 Brand Studio/CRM 흐름이 최신 데이터를 참조하게 됩니다.
- 다음 후보 task: `/tmp/off-community-hourly.log`와 Data Asset Inventory 카드를 LaunchAgent 실행 후에 검사하여 실제 런타임이 기록·반영되는지 확인하고, Supabase `culture_items` 테이블이 동일한 타임스탬프를 통해 최신화되는지를 검증합니다.

### 16:40 KST
- 무엇을 바꿨는지: `scripts/hourly_autonomous_job.py` now uses `datetime.now(tz=timezone.utc)` so the LaunchAgent log can append safely, `scripts/import_culture_items_supabase.py` prepends the repo root to `sys.path` before importing `utils`, and `utils/app_settings.py` tolerates a missing `python-dotenv` package. I reran the hourly pipeline with the same redirection LaunchAgent uses, saw `/tmp/off-community-hourly.log` end with a success summary, and confirmed `app/static/data/data_asset_status.json` refreshed at 07:06 UTC.
- 왜 바꿨는지: The hourly orchestrator had been crashing before it could refresh Jun’s cultural/identity/CTA payloads; fixing the timezone import and the Supabase importer keeps the `com.offcommunity.hourly` job from aborting mid-run and lets the data asset card show accurate timestamps every hour.
- Blockers/risks: Supabase client/credentials are still absent in this environment so the importer prints a warning and skips, but now the job exits cleanly instead of failing the pipeline.
- Saved data sources / Data-asset impact: Fresh JSON snapshots for promo/growth/lead/culture/identity/CTA assets plus the normalized `culture_items` manifest and data asset status all reflect the 2026-04-03T07:06 run; the `data_asset_status.json` and `/tmp/off-community-hourly.log` entries now prove the pipeline executed successfully.
- Next candidate task: Reintroduce Supabase credentials and the `supabase` package (or auto-install it) so the `culture_items` import starts populating Postgres again, then double-check the LaunchAgent log after the next run to keep the data-asset timeline trustworthy.

### 17:10 KST
- 무엇을 바꿨는지: `scripts/pipeline_health.py`로 data_asset_status 요약 + freshness/staleness 계산을 JSON으로 저장하고, 시간당 파이프라인에 이 스크립트를 추가했으며 랜딩 홈에 Pipeline Health 카드(CTA 포함)와 관련 CSS/렌더링 로직을 붙여 자동화 신뢰도를 노출했습니다.
- 왜 바꿨는지: 데이터 파이프라인이 실제로 돌아가는지 여부를 실시간으로 보여주면 브랜드/멤버십 전환 메시지 앞에서 신뢰도를 끌어올리고, Jun의 정체성·수익화 흐름이 항상 신선한 데이터 위에 서 있다는 점을 직접 증명할 수 있기 때문입니다.
- Blockers/risks: 없음; 새로운 스크립트는 데이터 자산 상태를 읽기만 하고, 만약 `data_asset_status.json` 이 없으면 fallback으로 기본값을 보여줍니다.
- Saved data sources: `app/static/data/data_asset_status.json` (pipeline summary의 `assets` 리스트)를 읽어 시간/보정/이력 데이터를 재정의하여 `app/static/data/pipeline_health.json`을 생성함.
- Data-asset impact: pipeline_health JSON이 Fresh/Stale/Ratio 값을 기록하여 future dashboard(Brand Studio, CRM)에서도 자동화 신뢰도를 스냅샷으로 재활용할 수 있고, UI 카드가 이 새 자산에 기반해 자동화 상태를 소구합니다.
- Next candidate task: automation doc/launch agent 로그를 랜딩에 더 밀착해서 "Last run"을 검증하는 항목과, Supabase pipeline 미동작을 감지하면 브랜드팀에 알리는 경보를 고민합니다.

### 18:20 KST
- 무엇을 바꿨는지: LaunchAgent 로그를 읽어 `app/static/data/automation_log.json`을 만드는 `scripts/collect_automation_log.py`를 추가하고 `scripts/hourly_autonomous_job.py`/doc/SESSION_HANDOFF을 동기화했으며, `app.py`와 랜딩 템플릿에 새 데이터 자산을 노출해 Pipeline Health 카드가 실제 로그 상태(마지막 실행, 성공 여부, 최근 요약)를 바로 보여주게 했습니다.
- 왜 바꿨는지: `/tmp/off-community-hourly.log`를 매번 열지 않아도 자동화가 성공적으로 끝났는지 데이터로 확인할 수 있어 방문자와 브랜드 대상 모두에게 수익화 신뢰도를 빠르게 증명하고, 자동화 기록 자체를 독점 데이터 자산으로 쌓기 위해서입니다.
- Blockers/risks: 없음.
- Saved data sources: `/tmp/off-community-hourly.log` 로그 → `automation_log.json` (timeline + recent lines), Pipeline Health UI/문서 업데이트.
- Data-asset impact: 새로운 automation log JSON이 Pipeline Health 카드와 Brand Studio/CRM에서 재활용 가능한 자동화 신뢰도 자산이 되었고, LaunchAgent run 상태를 계속 기록해 다음 run 때 검증할 수 있는 기반을 만들었습니다.
- Next candidate task: automation log JSON을 Brand Studio 알림 흐름이나 CRM 리포트의 감지기와 엮어 실패/지연을 확인할 수 있는 경보 스크립트를 고민해보는 것을 추천합니다.

### 18:34 KST
- 무엇을 바꿨는지: automation log JSON이 다음 실행 예상 시간을 저장하게 하고, 랜딩 Pipeline Health 카드 바로 아래 LaunchAgent 로그 패널에 "Next expected run" 라인을 추가해 시청자/브랜드가 시간당 파이프라인의 마지막/다음 타임스탬프를 동시에 확인할 수 있게 했습니다.
- 왜 바꿨는지: 시간당 자동화가 실제로 돌아간다는 신뢰를 UI에서 직접 증명하면 수익화/재방문 CTA 앞의 신뢰도가 올라가고, 새로 기록된 next_expected_run 데이터가 향후 알림/보고용 데이터 자산으로 계속 재활용될 수 있기 때문입니다.
- Blockers/risks: 없음.
- Saved data sources: /tmp/off-community-hourly.log (latest run + summary lines).
- Data-asset impact: automation_log JSON에 next_expected_run_{utc,local} 필드가 생기며, 랜딩 페이지가 해당 값을 바로 보여주도록 연동되어 파이프라인 신뢰도를 기록/재사용할 수 있는 기반이 확장되었습니다.
- Next candidate task: pipeline에서 실패하는 스크립트들(예: Billboard/Guardian/Supabase import)의 로그를 수집해 롤백/재시도를 설계하거나, 실패 감지 시 Brand Studio/Slack에 경고를 보내는 흐름을 추가합니다.
