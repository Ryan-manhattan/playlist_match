# Culture Pulse Refresh Cron

매 정시마다 문화 데이터를 다시 모아서 `culture.json`을 갱신하는 흐름을 만들었어. 이 데이터를 랜딩 페이지의 Culture Pulse 섹션에서 사용해서 "음악 × 영화" 기획 카피와 리포트를 바로 보여줄 수 있어.

### 스크립트
- `scripts/culture_data.py`: Supabase에서 월드컵 순위, 다이어리 게시글을 읽어와서 `top_tracks`, `film_diaries`, `hero_line` 같은 정보를 정리하고 `app/static/data/culture.json`에 저장.
- Supabase가 없으면 빈 데이터를 그대로 쓰기 때문에 로컬 개발에서도 UI가 깨지지 않아.

### 추천 크론
```
0 * * * * cd /Users/junkim/Projects/off_community && /usr/bin/env python3 scripts/culture_data.py >> /tmp/culture-cron.log 2>&1
```
- `/tmp/culture-cron.log`를 보면 성공/실패 여부를 확인할 수 있고, 매 시간 갱신되므로 `promo.json`과 함께 컬처 섹션의 캐피톤이 계속 바뀐다.
- 이미 `promo.json`을 새로 만드는 기존 자동화와 함께 두 스크립트를 등록하면 각 축(기획, 개발, 디자인, 보안)에서 변화를 보여주는 콘텐츠 흐름이 완성된다.
