# OAuth 인증 API 서버

Google, Apple, Naver, Kakao OAuth 2.0 인증을 지원하는 FastAPI 기반 REST API 서버입니다.

## 📁 프로젝트 구조

```
FestAPI/
├── app/
│   ├── core/                      # 핵심 설정 및 인프라
│   │   ├── config.py             # 환경 설정
│   │   └── database.py           # 인메모리 데이터베이스
│   ├── models/                    # 데이터 모델
│   │   └── user.py               # User, OAuthProvider, UserResponse
│   ├── schemas/                   # Pydantic 스키마
│   │   ├── auth.py               # OAuth UserInfo 스키마
│   │   └── user.py               # 사용자 스키마
│   ├── services/                  # 비즈니스 로직
│   │   ├── auth_service.py       # JWT 인증 서비스
│   │   └── auth/                 # OAuth 서비스들
│   │       ├── google.py         # Google OAuth
│   │       ├── apple.py          # Apple OAuth
│   │       ├── naver.py          # Naver OAuth
│   │       └── kakao.py          # Kakao OAuth
│   ├── routers/                   # API 라우터
│   │   ├── auth.py               # 인증 엔드포인트
│   │   ├── users.py              # 사용자 관리
│   │   └── protected.py          # 보호된 엔드포인트
│   ├── utils/                     # 유틸리티
│   │   └── dependencies.py       # FastAPI 의존성
│   ├── __main__.py                # Python 모듈 진입점
│   ├── main.py                    # FastAPI 앱
│   └── run.py                     # 서버 실행 스크립트
├── Dockerfile                     # Docker 이미지 빌드
├── docker-compose.yml             # Docker Compose 설정
├── .dockerignore                  # Docker 빌드 제외 파일
├── requirements.txt               # 의존성
├── .env.example                   # 환경 변수 예시
├── .gitignore                     # Git 제외 파일
└── README.md
```

## 📋 사전 준비사항

### Python 버전
- Python 3.8 이상 필요

### OAuth 앱 등록

각 OAuth 제공자에서 애플리케이션을 등록하고 인증 정보를 발급받아야 합니다.

#### Google OAuth
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 생성 또는 선택
3. "API 및 서비스" → "사용자 인증 정보"
4. "OAuth 2.0 클라이언트 ID" 생성
5. 승인된 리디렉션 URI: `http://localhost:8000/auth/google/callback`

#### Apple OAuth
1. [Apple Developer](https://developer.apple.com/) 가입 (연 $99)
2. Certificates, Identifiers & Profiles → Keys
3. "Sign in with Apple" 활성화된 키 생성
4. .p8 파일 다운로드 (한 번만 가능!)
5. Service IDs 생성 및 Return URL 설정: `http://localhost:8000/auth/apple/callback`

#### Naver OAuth
1. [네이버 개발자센터](https://developers.naver.com/) 접속
2. 애플리케이션 등록
3. 서비스 URL 및 콜백 URL 설정: `http://localhost:8000/auth/naver/callback`

#### Kakao OAuth
1. [카카오 개발자센터](https://developers.kakao.com/) 접속
2. 애플리케이션 추가
3. 플랫폼 설정에서 Redirect URI 등록: `http://localhost:8000/auth/kakao/callback`

## 🚀 설치 및 실행

### 방법 A: Docker 사용 (권장)

Docker를 사용하면 환경 설정 없이 바로 실행할 수 있습니다.

#### 1. .env 파일 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 실제 OAuth 값 입력
```

#### 2. Docker Compose로 실행

```bash
# 개발 모드로 실행 (코드 변경 시 자동 반영)
docker-compose up

# 백그라운드 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

#### 3. Docker만 사용 (Compose 없이)

```bash
# 이미지 빌드
docker build -t festapi .

# 컨테이너 실행
docker run -p 8000:8000 --env-file .env festapi
```

#### 프로덕션 모드 실행

```bash
# 4개의 워커로 실행
docker-compose --profile production up api-prod
```

### 방법 B: 로컬 환경에서 실행

#### 1. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 환경 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 실제 OAuth 값 입력
# (에디터로 .env 파일을 열어 수정)
```

`.env` 파일 예시:
```env
# JWT 설정
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
REDIRECT_URI_GOOGLE=http://localhost:8000/auth/google/callback

# Apple OAuth (선택)
APPLE_CLIENT_ID=com.yourcompany.yourapp.signin
APPLE_TEAM_ID=YOUR_TEAM_ID
APPLE_KEY_ID=YOUR_KEY_ID
APPLE_PRIVATE_KEY_PATH=./apple_private_key.p8
REDIRECT_URI_APPLE=http://localhost:8000/auth/apple/callback

# Naver OAuth (선택)
NAVER_CLIENT_ID=your-naver-client-id
NAVER_CLIENT_SECRET=your-naver-client-secret
REDIRECT_URI_NAVER=http://localhost:8000/auth/naver/callback

# Kakao OAuth (선택)
KAKAO_CLIENT_ID=your-kakao-client-id
KAKAO_CLIENT_SECRET=your-kakao-client-secret
REDIRECT_URI_KAKAO=http://localhost:8000/auth/kakao/callback
```

### 4. 서버 실행

```bash
# 방법 1: Python 모듈로 실행 (권장)
python -m app

# 방법 2: uvicorn 직접 사용
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 방법 3: run.py 직접 실행
python app/run.py
```

서버가 시작되면 다음 주소에서 접속 가능합니다:
- 홈페이지: http://localhost:8000
- API 문서 (Swagger): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

## 📖 API 엔드포인트

### 인증 (Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/google` | Google OAuth 로그인 시작 |
| GET | `/auth/google/callback` | Google OAuth 콜백 |
| GET | `/auth/apple` | Apple OAuth 로그인 시작 |
| POST | `/auth/apple/callback` | Apple OAuth 콜백 |
| GET | `/auth/naver` | Naver OAuth 로그인 시작 |
| GET | `/auth/naver/callback` | Naver OAuth 콜백 |
| GET | `/auth/kakao` | Kakao OAuth 로그인 시작 |
| GET | `/auth/kakao/callback` | Kakao OAuth 콜백 |
| GET | `/auth/me` | 현재 사용자 정보 조회 |
| PUT | `/auth/me` | 현재 사용자 정보 수정 |
| POST | `/auth/logout` | 로그아웃 (토큰 블랙리스트 처리) |
| POST | `/auth/refresh` | 리프레시 토큰으로 액세스 토큰 갱신 |
| POST | `/auth/cleanup-blacklist` | 만료된 블랙리스트 토큰 정리 |

### 사용자 (Users)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | 모든 사용자 조회 (인증 필요) |
| GET | `/users/{email}` | 특정 사용자 조회 (인증 필요) |

### 게시글 (Posts)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/posts/` | 게시글 작성 (인증 필요) |
| GET | `/posts/` | 게시글 목록 조회 (최신순) |
| GET | `/posts/me` | 내가 작성한 게시글 조회 (인증 필요) |
| GET | `/posts/{post_id}` | 게시글 상세 조회 |
| PUT | `/posts/{post_id}` | 게시글 수정 (작성자만, 인증 필요) |
| DELETE | `/posts/{post_id}` | 게시글 삭제 (작성자만, 인증 필요) |

### 보호된 엔드포인트 (Protected)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/protected/` | 보호된 엔드포인트 예제 |
| GET | `/protected/admin` | 관리자 전용 엔드포인트 예제 |

## 🧪 사용 예시

### 1. OAuth 로그인

브라우저에서 접속:
```
http://localhost:8000/auth/google
http://localhost:8000/auth/kakao
```

로그인 성공 시 응답:
```json
{
  "user": {
    "id": "google_123456789",
    "email": "user@example.com",
    "name": "홍길동",
    "picture": "https://...",
    "verified_email": true,
    "provider": "google",
    "provider_id": "123456789"
  },
  "access_token": "eyJhbGc..."
}
```

### 2. 인증된 API 호출

```bash
# 현재 사용자 정보 조회
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/auth/me

# 사용자 정보 수정
curl -X PUT \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"새이름"}' \
  http://localhost:8000/auth/me
```

### 3. 로그아웃

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/auth/logout
```

### 4. 토큰 갱신

```bash
# 리프레시 토큰으로 새로운 액세스 토큰 발급
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"YOUR_REFRESH_TOKEN"}' \
  http://localhost:8000/auth/refresh
```

### 5. 게시글 CRUD

```bash
# 게시글 작성
curl -X POST \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"제목","content":"내용"}' \
  http://localhost:8000/posts/

# 게시글 목록 조회
curl http://localhost:8000/posts/

# 내가 작성한 게시글 조회
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/posts/me

# 게시글 상세 조회
curl http://localhost:8000/posts/{post_id}

# 게시글 수정
curl -X PUT \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"수정된 제목"}' \
  http://localhost:8000/posts/{post_id}

# 게시글 삭제
curl -X DELETE \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/posts/{post_id}
```

## 🔧 개발 정보

### 기술 스택
- **Framework**: FastAPI 0.104.1
- **Authentication**: OAuth 2.0, JWT
- **Python**: 3.8+
- **Database**: In-Memory (개발용)
- **Containerization**: Docker, Docker Compose

### 주요 라이브러리
- `fastapi`: 웹 프레임워크
- `uvicorn`: ASGI 서버
- `pydantic`: 데이터 검증
- `PyJWT`: JWT 토큰 관리
- `httpx`: 비동기 HTTP 클라이언트
- `cryptography`: 암호화 (Apple OAuth)

## 🛠️ 문제 해결

### Docker 관련

#### 컨테이너가 시작되지 않는 경우
```bash
# 컨테이너 로그 확인
docker-compose logs api

# 컨테이너 재시작
docker-compose restart api

# 이미지 다시 빌드
docker-compose build --no-cache
docker-compose up
```

#### 포트 충돌
```bash
# Docker Compose에서 다른 포트 사용
# docker-compose.yml 수정: "8080:8000"
docker-compose up

# 또는 환경변수로 설정
PORT=8080 docker-compose up
```

#### 환경변수가 적용되지 않는 경우
```bash
# .env 파일이 올바른 위치에 있는지 확인
ls -la .env

# 컨테이너 재시작
docker-compose down
docker-compose up
```

### 로컬 실행 관련

#### 포트 충돌
```bash
# 다른 포트로 실행
uvicorn app.main:app --reload --port 8080
```

### OAuth 콜백 오류
1. OAuth 제공자 설정에서 리디렉션 URI 확인
2. `.env` 파일의 CLIENT_ID, CLIENT_SECRET 확인
3. 로컬호스트 포트 일치 여부 확인

### 패키지 설치 오류
```bash
pip install --upgrade pip setuptools wheel
pip cache purge
pip install -r requirements.txt
```

## 🔒 보안 기능

### 토큰 블랙리스트
- **로그아웃 시 토큰 무효화**: 로그아웃 시 액세스 토큰이 블랙리스트에 추가되어 재사용 방지
- **자동 검증**: 모든 API 요청 시 블랙리스트 확인
- **자동 정리**: `/auth/cleanup-blacklist` 엔드포인트로 만료된 블랙리스트 항목 정리 (7일 이상 경과)

### 토큰 관리
- **액세스 토큰**: 24시간 유효, 짧은 만료 시간으로 보안 강화
- **리프레시 토큰**: 7일 유효, 액세스 토큰 갱신에 사용
- **토큰 타입 검증**: access/refresh 토큰 타입을 구분하여 검증

## 📝 TODO

- [ ] 실제 데이터베이스 연동 (PostgreSQL, MySQL 등)
- [ ] Redis 기반 세션 및 블랙리스트 관리
- [x] 리프레시 토큰 구현
- [x] 토큰 블랙리스트 구현
- [ ] 사용자 권한 관리 (Role-based Access Control)
- [ ] API Rate Limiting
- [ ] 로깅 시스템
- [ ] 단위 테스트 및 통합 테스트

## 📄 License

MIT License

## 👨‍💻 Author

FestAPI Team
