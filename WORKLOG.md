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
