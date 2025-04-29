# Playlist Match

음악 취향 매칭 및 플레이리스트 공유 플랫폼

## 프로젝트 구조 (2024-04-29 기준)

```
playlist-match/
├── app/
│   ├── chart/
│   │   └── page.tsx        # 음악 차트 페이지 (차트 리스트, 모달, 헤더 포함)
│   ├── login/
│   │   └── page.tsx        # 로그인 페이지
│   ├── signup/
│   │   └── page.tsx        # 회원가입 페이지
│   ├── components/
│   │   ├── Header.tsx      # 공통 헤더 컴포넌트
│   │   └── TrackModal.tsx  # 트랙 상세 정보 모달 컴포넌트
│   ├── layout.tsx          # 전체 레이아웃
│   ├── page.tsx            # 랜딩(메인) 페이지
│   ├── globals.css         # 글로벌 스타일
│   └── favicon.ico         # 파비콘
├── src/
│   ├── components/
│   │   └── chart/
│   │       └── ChartSection.tsx # 차트 섹션 컴포넌트 (Spotify API fetch, 콘솔로그 포함)
│   └── lib/
│       └── spotify.ts      # Spotify API 유틸리티 함수 (getTopTracks 등 구현)
├── public/
├── .env                    # 환경 변수 (Spotify API 키 등, 현재 미존재)
└── package.json            # 프로젝트 의존성
```

## 현재 진행 상황 (2024-04-29 기준)

### 완료된 작업
1. 프로젝트 기본 구조 설정 (Next.js, TypeScript, TailwindCSS, ESLint)
2. chart, login, signup, 랜딩(메인) 페이지 및 라우팅 정상화
3. app 폴더 구조 정리 및 중첩 app 폴더 제거
4. ChartSection, spotify.ts 등 주요 컴포넌트/유틸리티 구현
5. next.config.js 환경변수, 이미지 도메인, 경로 별칭 등 설정
6. 콘솔로그로 각 이벤트/에러 추적 가능하도록 구현
7. 차트 페이지 UI/UX 개선
   - 트랙 상세 정보 모달 구현
   - 반응형 디자인 적용
   - 로딩/에러 상태 UI 개선
   - 헤더 컴포넌트 통합

### 오늘 진행한 작업 (2024-04-29)
1. 차트 페이지 개선
   - 헤더 컴포넌트 추가 및 스타일링
   - 트랙 상세 정보 모달 UI 개선 (반투명 배경, 좌우 분할 레이아웃)
   - 차트 리스트 디자인 개선 (그리드 시스템, 호버 효과)
   - 로딩/에러 상태 UI 개선
2. 코드 구조 개선
   - TypeScript 인터페이스 추가 (TrackModalInfo 등)
   - 컴포넌트 구조 최적화
3. README 최신화

### 발견된 문제/이슈
1. .env 파일 미존재로 Spotify API 연동 불가
2. 환경변수는 next.config.js 및 코드에서 참조, 실제 값 필요
3. ChartSection 등에서 콘솔로그로 상태 추적 가능

### 해야 할 작업 (우선순위)
1. 차트 데이터 연동 개선
   - Spotify API 연동 최적화
   - 에러 처리 및 재시도 로직 구현
   - 데이터 캐싱 구현

2. 곡 정보 분석 기능 강화
   - 곡 상세 분석 항목 확장 (BPM, 키, 장르 등)
   - 오디오 특성 분석 API 연동
   - 분석 결과 시각화 구현

3. 플레이리스트 관리 기능 개발
   - 플레이리스트 생성/수정/삭제 기능
   - 곡 추가/제거 기능
   - 플레이리스트 공유 기능

4. 음악 취향 분석 시스템 개발
   - 사용자 플레이리스트 분석 알고리즘
   - 곡 선호도 패턴 분석
   - 장르/아티스트 선호도 가중치 시스템

5. 매칭 시스템 구현
   - 사용자 간 음악 취향 유사도 계산
   - 매칭 추천 알고리즘 개발
   - 매칭 결과 표시 UI 구현

6. 테스트 및 문서화
   - 단위 테스트 작성
   - E2E 테스트 구현
   - API 문서화
   - 사용자 가이드 작성

## 환경 설정

### 필수 환경 변수 (반드시 .env 파일로 관리, gitignore에 포함됨)
```env
NEXT_PUBLIC_SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REFRESH_TOKEN=your_refresh_token
```

## 실행 방법

```bash
npm install
npm run dev
```

## 알려진 이슈
1. .env 미존재로 인한 API 연동 불가
2. 환경변수 값 누락 시 Spotify API fetch 실패

---

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
