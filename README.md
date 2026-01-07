# FestAPI - OAuth 인증 서버

Google, Apple, Naver, Kakao OAuth 2.0 인증을 지원하는 FastAPI 기반 REST API 서버

## ✨ 주요 기능

- 🔐 **OAuth 2.0 소셜 로그인** - Google, Apple, Naver, Kakao
- 🎫 **JWT 인증** - Access Token (24h) + Refresh Token (7d)
- 🛡️ **토큰 블랙리스트** - 로그아웃 시 토큰 무효화
- 📝 **게시글 CRUD** - 인증 기반 게시글 관리
- 🐳 **Docker 지원** - 컨테이너화된 배포
- 🚀 **CI/CD** - GitHub Actions 자동화

## 🚀 빠른 시작

### Docker 사용 (권장)

```bash
# 환경 설정
cp .env.example .env
# .env 파일 편집하여 OAuth 키 입력

# 실행
docker-compose up

# 백그라운드 실행
docker-compose up -d
```

### 로컬 실행

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 설정
cp .env.example .env
# .env 파일 편집

# 서버 실행
python -m app
```

서버 실행 후: http://localhost:8000/docs

## 📡 API 엔드포인트

### 인증
- `GET /auth/{provider}` - OAuth 로그인 (google, apple, naver, kakao)
- `GET /auth/{provider}/callback` - OAuth 콜백
- `POST /auth/refresh` - 토큰 갱신
- `POST /auth/logout` - 로그아웃
- `GET /auth/me` - 내 정보 조회
- `PUT /auth/me` - 내 정보 수정

### 게시글
- `POST /posts/` - 게시글 작성 🔒
- `GET /posts/` - 게시글 목록
- `GET /posts/me` - 내 게시글 🔒
- `GET /posts/{id}` - 게시글 조회
- `PUT /posts/{id}` - 게시글 수정 🔒
- `DELETE /posts/{id}` - 게시글 삭제 🔒

🔒 = 인증 필요

## 🔧 환경 변수

```env
# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
REDIRECT_URI_GOOGLE=http://localhost:8000/auth/google/callback

# Apple OAuth (선택)
APPLE_CLIENT_ID=com.yourcompany.app
APPLE_TEAM_ID=YOUR_TEAM_ID
APPLE_KEY_ID=YOUR_KEY_ID
APPLE_PRIVATE_KEY_PATH=./apple_private_key.p8
REDIRECT_URI_APPLE=http://localhost:8000/auth/apple/callback

# Naver OAuth (선택)
NAVER_CLIENT_ID=your-client-id
NAVER_CLIENT_SECRET=your-client-secret
REDIRECT_URI_NAVER=http://localhost:8000/auth/naver/callback

# Kakao OAuth (선택)
KAKAO_CLIENT_ID=your-client-id
KAKAO_CLIENT_SECRET=your-client-secret
REDIRECT_URI_KAKAO=http://localhost:8000/auth/kakao/callback
```

## 🧪 테스트

```bash
# 테스트 실행
pytest tests/ -v

# 커버리지 포함
pytest tests/ --cov=app
```

## 🚀 CI/CD

GitHub Actions로 자동화된 파이프라인:

- **CI**: 테스트, 린팅, 보안 스캔 (Python 3.9, 3.10, 3.11)
- **Docker**: 이미지 빌드 & GitHub Container Registry 푸시
- **Deploy**: SSH/AWS/GCP 자동 배포

## 📁 프로젝트 구조

```
FestAPI/
├── .github/workflows/     # CI/CD 파이프라인
├── app/
│   ├── core/             # 설정 및 DB
│   ├── models/           # 데이터 모델
│   ├── schemas/          # Pydantic 스키마
│   ├── services/         # 비즈니스 로직
│   │   └── auth/         # OAuth 서비스
│   ├── routers/          # API 엔드포인트
│   └── main.py           # FastAPI 앱
├── tests/                # 테스트
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🔒 보안

- JWT 기반 인증 (Access + Refresh Token)
- 토큰 블랙리스트 (로그아웃 시 무효화)
- OAuth 2.0 표준 준수
- 환경 변수로 민감 정보 관리
- 자동 보안 스캔 (Bandit, Safety, Trivy)

## 📝 OAuth 앱 등록

### Google
[Google Cloud Console](https://console.cloud.google.com/) → API 및 서비스 → OAuth 2.0 클라이언트 ID 생성

### Apple
[Apple Developer](https://developer.apple.com/) → Keys → Sign in with Apple 활성화

### Naver
[네이버 개발자센터](https://developers.naver.com/) → 애플리케이션 등록

### Kakao
[카카오 개발자센터](https://developers.kakao.com/) → 애플리케이션 추가

## 📄 라이선스

MIT License

## 👨‍💻 Author

FestAPI Team
