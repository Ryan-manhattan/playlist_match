# Playlist Match

음악 취향 매칭 및 플레이리스트 공유 플랫폼

## 프로젝트 구조 (2024-04-30 기준)

```
playlist-match/
├── app/
│   ├── api/
│   │   └── auth/
│   │       └── [...nextauth]/
│   │           └── route.ts  # NextAuth API 라우트
│   ├── chart/
│   │   └── page.tsx        # 음악 차트 페이지
│   ├── login/
│   │   └── page.tsx        # 로그인 페이지
│   ├── signup/
│   │   └── page.tsx        # 회원가입 페이지
│   ├── components/
│   │   ├── Header.tsx      # 공통 헤더 컴포넌트 (로그인 상태 관리 포함)
│   │   └── TrackModal.tsx  # 트랙 상세 정보 모달 컴포넌트
│   ├── client-layout.tsx   # 클라이언트 레이아웃 (SessionProvider)
│   ├── layout.tsx          # 전체 레이아웃
│   ├── page.tsx            # 랜딩(메인) 페이지
│   ├── globals.css         # 글로벌 스타일
│   └── favicon.ico         # 파비콘
├── prisma/
│   ├── schema.prisma       # Prisma 스키마
│   └── migrations/         # 데이터베이스 마이그레이션
├── src/
│   ├── components/
│   │   └── chart/
│   │       └── ChartSection.tsx # 차트 섹션 컴포넌트
│   │
│   └── lib/
│       └── spotify.ts      # Spotify API 유틸리티 함수
├── middleware.ts           # 인증 미들웨어 (보호된 라우트)
├── next.config.js         # Next.js 설정
├── .env                   # 환경 변수
└── package.json           # 프로젝트 의존성
```

## 현재 진행 상황 (2024-04-30 기준)

### 완료된 작업
1. 프로젝트 기본 구조 설정
   - Next.js, TypeScript, TailwindCSS, ESLint
   - Prisma ORM 설정
   - NextAuth.js 설정
   - PostgreSQL 데이터베이스 연결

2. 사용자 인증 시스템 구축
   - Google OAuth 로그인 구현
   - NextAuth 설정 및 환경변수 구성
   - 사용자 세션 관리
   - 보호된 라우트 설정 (미들웨어)

3. 데이터베이스 설정
   - Prisma 스키마 정의 (User, Account, Session, Playlist, Track 모델)
   - 초기 마이그레이션 실행
   - PostgreSQL 서버 설정

4. UI/UX 개선
   - 로그인 페이지 구현
   - 헤더에 사용자 프로필 표시
   - 드롭다운 메뉴 (프로필, 플레이리스트, 로그아웃)
   - 로딩 상태 표시

### 최근 완료/진행된 작업

1. 공통 레이아웃 개선
   - Header, Footer 컴포넌트를 `app/layout.tsx`에 공통으로 추가하여 모든 페이지에서 자동으로 표시
   - 각 페이지에서 Header/Footer 중복 import 및 사용 코드 제거

2. 프로필 페이지(/profile)
   - 사용자 정보(이름, 프로필 이미지) 표시 및 수정 기능 구현
   - 프로필 이미지 파일 업로드 및 DB 연동
   - API 연동(GET/PUT /api/user)
   - 메인 페이지로 돌아가기 버튼 추가

3. 플레이리스트 페이지(/playlists)
   - UI/UX 구현
     - 카드/폴더형 UI로 플레이리스트 목록 표시
     - 플레이리스트 생성 모달 구현 (제목, 설명, 썸네일)
     - 로딩/에러 상태 처리
     - 반응형 그리드 레이아웃

   - 기능 구현
     - 플레이리스트 목록 조회 (GET /api/playlists)
     - 플레이리스트 생성 (POST /api/playlists)
     - 썸네일 이미지 업로드 처리
     - 트랙 정렬 기능 (생성일 기준 오름차순)

   - 데이터베이스
     - Playlist 모델 스키마 업데이트
       - thumbnail 필드 추가 (String, Optional)
       - Track 모델과 N:M 관계 설정
     - 마이그레이션 실행 및 적용

   - 타입 시스템
     - Prisma 생성 타입 동기화
     - 커스텀 타입 정의 (PlaylistWithThumbnail, PlaylistWithDetails)
     - 타입 매핑 함수 구현 (mapPlaylistWithTracks)

   - API 엔드포인트
     - GET /api/playlists: 사용자의 플레이리스트 목록 조회
     - POST /api/playlists: 새 플레이리스트 생성
     - GET /api/playlists/[id]: 특정 플레이리스트 상세 조회

4. 기타
   - 모든 페이지에서 Header/Footer가 중복 렌더링되는 문제 해결
   - 기본 썸네일 이미지는 `/public/default-playlist.png`로 지정
   - Prisma Client 타입 오류 해결 (thumbnail 필드 관련)

5. 2024-05-XX: app/lib로 authOptions, prisma 이동 및 tsconfig.json include에 app/lib/**/* 추가, import 오류 해결
   - app/api/user/route.ts 등에서 '../lib/authOptions', '../lib/prisma' import 시 모듈을 찾지 못하는 오류 발생
   - lib/authOptions.ts, lib/prisma.ts를 app/lib/로 이동
   - import 경로를 '../lib/authOptions', '../lib/prisma'로 수정
   - tsconfig.json의 include에 'app/lib/**/*' 추가하여 타입스크립트가 app/lib 폴더 인식하도록 조치
   - Next.js app router 구조에서 app/lib로 핵심 모듈 이동이 가장 안전함

### 해야 할 작업 (우선순위)
1. 플레이리스트 기능 고도화
   - 플레이리스트 수정/삭제 기능
   - 플레이리스트 상세 페이지
   - 트랙 추가/관리 기능

2. 음악 차트 페이지 구현 (/chart)
   - Spotify API 연동
   - 인기 음악 목록 표시
   - 플레이리스트에 추가 기능

3. 추가 인증 기능
   - Spotify OAuth 연동
   - 이메일/비밀번호 회원가입

4. 기타 개선사항
   - 에러/로딩 UX 개선
   - 테스트 코드 작성
   - 코드 리팩토링

## 환경 설정

### node_modules 설치 및 경로 문제 주의
- node_modules가 설치되어 있지 않으면 타입 선언, 모듈 해석, import 관련 오류가 발생할 수 있음
- 반드시 프로젝트 루트(playlist-match)에서 npm install 실행 후, .next 캐시 삭제 및 서버 재시작 필요
- import 경로 오류 발생 시, node_modules 설치 여부와 실제 파일 경로/이름을 우선 점검할 것

### 필수 환경 변수 (.env)
```env
# Database
DATABASE_URL="postgresql://kimjunhyeong@localhost:5432/playlist_match?schema=public"

# NextAuth.js
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your_nextauth_secret"

# OAuth Providers
GOOGLE_CLIENT_ID="your_google_client_id"
GOOGLE_CLIENT_SECRET="your_google_client_secret"

# Spotify API (추후 설정)
NEXT_PUBLIC_SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REFRESH_TOKEN=
```

## 실행 방법

```bash
# PostgreSQL 서버 시작
brew services start postgresql@14

# 의존성 설치
npm install

# 데이터베이스 마이그레이션
npx prisma migrate dev

# 개발 서버 실행
npm run dev
```

## 알려진 이슈
1. 플레이리스트 관련
   - 플레이리스트 수정/삭제 기능 미구현
   - 트랙 추가/삭제/순서 변경 기능 미구현
   - 플레이리스트 공유 기능 미구현
   - 플레이리스트 상세 페이지 미구현

2. 음악 차트 관련
   - Spotify API 연동 미구현
   - 인기 음악 목록 표시 미구현
   - 음악 검색 기능 미구현
   - 음악 미리듣기 기능 미구현

3. 사용자 경험
   - 로딩/에러 상태 UI 개선 필요
   - 반응형 디자인 개선 필요
   - 다크 모드 지원 필요
   - 접근성 개선 필요

4. 기술적 이슈
   - 테스트 코드 부재
   - 성능 최적화 필요
   - 코드 리팩토링 필요
   - 타입 안정성 개선 필요

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
