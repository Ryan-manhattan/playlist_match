# 음악 자동 영상 → YouTube 게시

`/music-video`에서 음원 하나를 올리면 OFF THE COMMUNITY가 기본 16:9 타이틀 카드를 만들고, 1080p MP4를 렌더링한 뒤 연결된 YouTube 채널에 게시합니다. 기본 공개 상태는 `private`입니다.

이 기능은 읽기 전용 `YOUTUBE_API_KEY`가 아닌 기존 Google Web OAuth 클라이언트의 `GOOGLE_CLIENT_ID`와 `GOOGLE_CLIENT_SECRET`을 사용합니다. 서버에 저장되는 OAuth 토큰은 해당 채널에 게시할 수 있으므로 Git에 추가하거나 브라우저로 보내면 안 됩니다.

## Hermes Drive inbox workflow

Hermes가 요청에 따라 로컬에서 처리하는 공식 음원 워크플로는 아래 Drive 폴더만
입력함으로 사용합니다.

```text
https://drive.google.com/drive/folders/1XklZ6JTuaCrUeAxAchlwdmyTAG5MatlS
```

- 음원은 폴더 최상위에 올린다. 지원 형식은 MP3, WAV, M4A, FLAC, AAC, OGG다.
- 커버 이미지는 음원과 확장자를 뺀 이름이 정확히 같아야 한다. 예:
  `Night Tide.mp3` + `Night Tide.png`.
- Hermes는 최신 음원을 로컬로 내려받아 1920×1080 영상으로 렌더링한다. OFF 로고는
  중앙·세로 35% 위치에 고정하고, 곡 제목을 바로 아래에 표시한다.
- YouTube 업로드에 성공한 MP4와 원본 음원은 같은 Drive 폴더의 `upload_완료` 하위 폴더에 저장/이동한다. 따라서 최상위 폴더에는 아직 처리하지 않은 음원만 남는다.
  같은 이름의 커버 이미지는 입력 폴더에 유지한다.
- YouTube 채널 계정과 Drive 소유 계정이 다르면, Drive 입력 폴더를 게시 계정에
  **편집자** 권한으로 공유해야 한다.
- OAuth 동의 범위에는 `https://www.googleapis.com/auth/youtube.upload`와
  `https://www.googleapis.com/auth/drive`가 모두 필요하다.

일반 명령은 `폴더에 음원 올렸으니 영상 만들어서 업로드해`다. 기본 공개 상태는
`private`이며, 같은 음원의 중복 업로드는 SHA-256 기록으로 차단된다.

## 로컬 설정

1. Google Cloud Console에서 이 앱의 기존 **Web application** OAuth 클라이언트를 엽니다. **YouTube Data API v3**를 같은 프로젝트에서 사용 설정하고 OAuth 동의 화면을 완료합니다. 앱이 Testing 상태라면 채널 소유자 Google 계정을 테스트 사용자로 추가합니다.
2. 해당 OAuth 클라이언트의 **Authorized redirect URIs**에 아래 URI를 정확히 추가합니다.

   ```text
   http://localhost:5000/api/youtube/upload/callback
   ```

3. `.env`에 기존 OAuth 클라이언트 값과 게시 설정을 둡니다. 값 자체는 공유하거나 커밋하지 않습니다.

   ```dotenv
   GOOGLE_CLIENT_ID=your-existing-google-oauth-client-id
   GOOGLE_CLIENT_SECRET=your-existing-google-oauth-client-secret
   YOUTUBE_UPLOAD_REDIRECT_URI=http://localhost:5000/api/youtube/upload/callback
   YOUTUBE_UPLOAD_ALLOWED_USER_IDS=guest-demo-user
   YOUTUBE_UPLOAD_TOKEN_FILE=data/youtube_upload_token.json
   ```

   `YOUTUBE_UPLOAD_ALLOWED_USER_IDS`는 쉼표로 구분한 앱 사용자 ID의 allow-list입니다. 현재 로컬 자동 로그인은 `guest-demo-user`를 사용하므로 위 값으로 연결과 게시를 테스트할 수 있습니다. 실제 인증 사용자는 `/api/me`에서 ID를 확인해 추가합니다.
4. 서버를 재시작하고 `/music-video`를 엽니다. **YOUTUBE 채널 연결**을 누르고, 게시할 채널 소유자 Google 계정으로 `youtube.upload` 권한을 승인합니다. Google이 `/api/youtube/upload/callback`으로 돌아오면 서버가 토큰을 `YOUTUBE_UPLOAD_TOKEN_FILE`에 저장합니다.
5. 연결 상태가 표시되면 음원, 제목, 설명, 태그, 공개 상태를 입력해 게시합니다. 완료된 작업의 YouTube 링크와 생성 MP4 다운로드 링크는 작업 상태에 포함됩니다.

`YOUTUBE_UPLOAD_REDIRECT_URI`는 필수입니다. 반드시 절대 `http`/`https` URL이어야 하며, 경로는 정확히 `/api/youtube/upload/callback`이어야 합니다. 쿼리 문자열과 fragment는 허용되지 않습니다.

## Render 설정

1. Render 서비스의 Environment에 다음 값을 설정합니다. `GOOGLE_CLIENT_ID`와 `GOOGLE_CLIENT_SECRET`에는 이미 사용 중인 Web OAuth 클라이언트 값을 사용합니다.

   ```text
   GOOGLE_CLIENT_ID
   GOOGLE_CLIENT_SECRET
   YOUTUBE_UPLOAD_REDIRECT_URI=https://your-service.onrender.com/api/youtube/upload/callback
   YOUTUBE_UPLOAD_ALLOWED_USER_IDS=your-production-app-user-id
   YOUTUBE_UPLOAD_TOKEN_FILE=/var/data/youtube_upload_token.json
   ```

2. Render Persistent Disk를 `/var/data`에 연결합니다. 연결하지 않으면 배포 또는 재시작 후 OAuth 토큰이 사라져 채널을 다시 연결해야 합니다.
3. Google Cloud Console의 같은 OAuth 클라이언트에 다음 production redirect URI를 추가합니다. Render 환경 변수와 한 글자도 다르면 안 됩니다.

   ```text
   https://your-service.onrender.com/api/youtube/upload/callback
   ```

4. Production에서는 실제 운영자 ID만 `YOUTUBE_UPLOAD_ALLOWED_USER_IDS`에 넣고 `AUTO_LOGIN_BYPASS_AUTH=false`로 설정합니다. allow-list가 비어 있으면 누구도 연결하거나 게시할 수 없습니다.
5. 배포 후 allow-list에 든 운영자가 `/music-video`에서 채널을 한 번 연결합니다. 서버 토큰은 모든 허가된 운영자가 같은 YouTube 채널로 게시할 때 사용됩니다.

## API 동작과 문제 해결

- `GET /api/youtube/upload/status`: OAuth 설정, 채널 연결, 현재 사용자의 게시 권한을 확인합니다.
- `GET /api/youtube/upload/authorize`: allow-list 사용자만 Google 동의 흐름을 시작합니다.
- `GET /api/youtube/upload/callback`: Google OAuth callback입니다. 상태 값과 시작한 사용자 ID를 검증한 뒤에만 토큰을 저장합니다.
- `POST /api/music-video/publish`: 업로드 작업을 시작합니다. `audio`는 필수이고 `title`, `description`, `tags`, `privacy_status`는 선택입니다. `privacy_status`는 `private`, `unlisted`, `public` 중 하나이며 기본값은 `private`입니다.

채널 연결이 필요하면 게시 API는 `409`와 `authorization_url`을 반환합니다. OAuth 설정 또는 redirect URI가 누락되면 상태 화면에서 설정 필요로 표시됩니다. API 키만 설정한 경우에는 업로드할 수 없습니다.

자신이 게시 권리를 가진 음원, 이미지, 메타데이터만 업로드하세요.
