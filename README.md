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

### 오늘 진행한 작업 (2024-04-30)
1. 사용자 인증 시스템 구축
   - Google OAuth 로그인 구현
   - NextAuth 설정
   - SessionProvider 추가
   - 미들웨어로 보호된 라우트 설정

2. 데이터베이스 설정
   - PostgreSQL 설치 및 설정
   - Prisma 스키마 정의
   - 초기 마이그레이션 실행

3. UI 개선
   - 헤더 컴포넌트에 로그인 상태 표시
   - 사용자 프로필 드롭다운 메뉴 구현
   - 로그아웃 기능 구현

### 발견된 문제/이슈
1. 환경변수 설정 필요 (.env 파일)
   - DATABASE_URL
   - NEXTAUTH_URL
   - NEXTAUTH_SECRET
   - GOOGLE_CLIENT_ID
   - GOOGLE_CLIENT_SECRET

2. 보호된 라우트
   - /profile
   - /playlists/*
   - /chart

### 해야 할 작업 (우선순위)
1. 프로필 페이지 구현 (/profile)
   - 사용자 정보 표시
   - 프로필 수정 기능

2. 플레이리스트 페이지 구현 (/playlists)
   - 플레이리스트 목록 표시
   - 플레이리스트 생성/수정/삭제

3. 음악 차트 페이지 구현 (/chart)
   - Spotify API 연동
   - 인기 음악 목록 표시
   - 플레이리스트에 추가 기능

4. 추가 인증 기능
   - Spotify OAuth 연동
   - 이메일/비밀번호 회원가입

## 환경 설정

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
1. 프로필 페이지 미구현
2. 플레이리스트 기능 미구현
3. Spotify API 연동 미구현

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
