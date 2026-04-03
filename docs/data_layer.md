# Data Layer (Supabase-ready)

이 프로젝트는 Supabase가 잠시 비활성 상태여도 나중에 다시 붙일 수 있도록, 로컬 데이터 저장을 3단계로 생각합니다.

## 1. raw
- 외부/내부에서 가져온 원본 스냅샷
- 예: RSS, 차트 API, 내부 로그 원문
- 목적: 나중에 재분석 가능하도록 원본 보관

## 2. normalized
- 서로 다른 소스를 공통 스키마로 맞춘 층
- 현재 예시: `data/normalized/culture_items.jsonl`
- 공통 필드:
  - `id`
  - `source`
  - `source_type`
  - `external_id`
  - `title`
  - `creator`
  - `url`
  - `published_at`
  - `summary`
  - `tags`
  - `raw_ref`
  - `collected_at`
  - `status`
  - `metadata`

## 3. derived
- 웹사이트 UI나 리포트가 바로 쓰는 파생 데이터
- 예:
  - `app/static/data/*.json`
  - `data/derived/culture_items_latest.json`
  - `data/derived/culture_items_manifest.json`

## Current implementation
- `scripts/build_culture_items.py`
  - `culture.json`
  - `culture_rss.json`
  - `billboard_hot100.json`
  - `deezer_chart.json`
  를 읽어 `culture_items` 공통 스키마로 정규화합니다.
- 출력:
  - `data/normalized/culture_items.jsonl`
  - `data/derived/culture_items_latest.json`
  - `data/derived/culture_items_manifest.json`

## Why this matters
이 구조를 먼저 잡아두면:
1. Supabase 복구 후 `culture_items` 같은 테이블로 이관이 쉬워지고
2. UI 변경과 데이터 자산 축적을 분리할 수 있고
3. Jun의 문화/정체성 데이터를 장기적으로 쌓아 브랜드 자산으로 만들 수 있습니다.
