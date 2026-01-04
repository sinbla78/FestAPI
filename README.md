# OAuth FastAPI 서버 실행 가이드

## 📋 사전 준비사항

### 1. Python 설치 확인
```bash
python --version  # Python 3.8 이상 필요합니다.
```

### 2. OAuth 앱 등록
각 서비스에서 OAuth 앱을 등록하고 클라이언트 ID, 시크릿을 발급받아야 합니다.

**Google Cloud Console**
- https://console.cloud.google.com/
- OAuth 2.0 클라이언트 ID 생성
- 승인된 리디렉션 URI: `http://localhost:8000/auth/google/callback`

**Apple Developer**
- https://developer.apple.com/
- Sign In with Apple 설정
- 리디렉션 URI: `http://localhost:8000/auth/apple/callback`

**네이버 개발자센터**
- https://developers.naver.com/
- 애플리케이션 등록
- 콜백 URL: `http://localhost:8000/auth/naver/callback`

**카카오 개발자센터**
- https://developers.kakao.com/
- 애플리케이션 추가
- Redirect URI: `http://localhost:8000/auth/kakao/callback`

## 🚀 실행 방법

### 방법 1: 자동 설정 스크립트 사용

```bash
# 스크립트 실행 권한 부여
chmod +x setup.sh

# 자동 설정 실행
./setup.sh
```

### 방법 2: 수동 설정

#### 1단계: 가상환경 생성 및 활성화
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 2단계: 패키지 설치
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3단계: 환경설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (실제 OAuth 값 입력)
nano .env  # 또는 원하는 에디터 사용
```

#### 4단계: 프로젝트 구조 확인
```
프로젝트/
├── main.py
├── requirements.txt
├── .env
├── .env.example
├── setup.sh
└── app/
    ├── __init__.py
    ├── models.py
    ├── config.py
    ├── auth.py           # 기존 파일
    ├── apple_auth.py     # 기존 파일
    ├── naver_auth.py     # 새로 생성
    ├── kakao_auth.py     # 새로 생성
    ├── database.py       # 기존 파일
    └── routers/
        ├── __init__.py
        ├── auth.py
        ├── protected.py
        └── users.py
```

## ▶️ 서버 실행

### 개발 서버 실행
```bash
uvicorn main:app --reload
```

### 프로덕션 서버 실행
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 포트 변경
```bash
uvicorn main:app --reload --port 3000
```

## 📖 API 문서 확인

서버가 실행되면 다음 URL에서 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 API 테스트

### 1. 헬스 체크
```bash
curl http://localhost:8000/health
```

### 2. OAuth 로그인 테스트
브라우저에서 다음 URL 접속:
- Google: http://localhost:8000/auth/google
- Apple: http://localhost:8000/auth/apple
- 네이버: http://localhost:8000/auth/naver
- 카카오: http://localhost:8000/auth/kakao

### 3. 보호된 엔드포인트 테스트
```bash
# 로그인 후 받은 토큰 사용
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/protected/
```

## 🔧 문제 해결

### 포트 충돌 오류
```bash
# 다른 포트로 실행
uvicorn main:app --reload --port 8080
```

### 패키지 설치 오류
```bash
# pip 업그레이드
pip install --upgrade pip setuptools wheel

# 캐시 클리어 후 재설치
pip cache purge
pip install -r requirements.txt
```

### OAuth 콜백 오류
1. 각 OAuth 서비스에서 리디렉션 URI가 정확히 설정되었는지 확인
2. .env 파일의 CLIENT_ID, CLIENT_SECRET 값 확인
3. 서버가 실제로 실행 중인 포트와 콜백 URL 포트 일치 확인

## 📝 추가 개발 사항

현재 구현에서 추가로 필요한 부분들:
1. `app/auth.py` - 기존 Google 인증 서비스
2. `app/apple_auth.py` - 기존 Apple 인증 서비스  
3. `app/database.py` - 데이터베이스 연결 및 사용자 관리
4. JWT 토큰 생성/검증 로직
5. 세션 관리 시스템