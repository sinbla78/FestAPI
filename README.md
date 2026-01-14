# FestAPI - 기간제 인력 관리 시스템

FastAPI 기반 기간제 인력 관리 REST API 서버

## ✨ 주요 기능

- 👤 **이중 인증 시스템** - 관리자/사용자 분리된 인증
- 🔐 **JWT 인증** - Access Token (24h) + Refresh Token (7d)
- 🌐 **OAuth 2.0 지원** - Google, Apple, Naver, Kakao 소셜 로그인
- 🆕 **첫 로그인 체크** - 초기 정보 입력 플로우
- 👥 **기간제 인력 관리** - 인적사항 등록/수정/검색
- 🏢 **부서 관리** - 부서별 인력 관리
- 🔑 **계정 관리** - 관리자의 사용자 계정 CRUD
- 📝 **게시글 관리** - 사용자 게시글 작성 및 관리
- 🐳 **Docker 지원** - 컨테이너화된 배포

## 📋 시스템 요구사항

- Python 3.9 이상
- PostgreSQL 12 이상
- Docker & Docker Compose (선택)

## 🚀 초기 세팅 및 실행 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd FestAPI
```

### 2. 환경 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (아래 필수 항목 설정)
# - DATABASE_URL: PostgreSQL 연결 URL
# - JWT_SECRET_KEY: JWT 암호화 키 (랜덤 문자열)
```

#### .env 필수 설정 항목

```env
# 환경 설정
ENVIRONMENT=development
DEBUG=true

# 데이터베이스 (필수)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/festapi

# JWT 설정 (필수)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS 설정
CORS_ORIGINS=["*"]

# OAuth 설정 (선택 - OAuth 사용 시에만 필요)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
REDIRECT_URI_GOOGLE=http://localhost:8000/auth/google/callback
# ... (기타 OAuth 설정)
```

### 3-A. Docker로 실행 (권장)

```bash
# Docker Compose로 실행 (PostgreSQL + FastAPI)
docker-compose up -d

# 로그 확인
docker-compose logs -f app

# 중지
docker-compose down
```

서버 실행 후: http://localhost:8000/docs

### 3-B. 로컬 환경에서 실행

#### 3-1. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

#### 3-2. 의존성 설치

```bash
# 개발 환경 (권장)
pip install -r requirements-dev.txt

# 또는 프로덕션 환경
pip install -r requirements-prod.txt
```

#### 3-3. 데이터베이스 설정

```bash
# PostgreSQL 데이터베이스 생성
createdb festapi

# 또는 psql로 접속하여
# CREATE DATABASE festapi;
```

#### 3-4. 데이터베이스 마이그레이션

```bash
# 마이그레이션 실행
alembic upgrade head

# 마이그레이션 파일 생성 (모델 변경 시)
alembic revision --autogenerate -m "description"
```

#### 3-5. 서버 실행

```bash
# 개발 서버 실행
python -m app

# 또는 uvicorn으로 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

서버 실행 후: http://localhost:8000/docs

## 📡 API 엔드포인트

### 관리자 (Manager)
- `POST /manager/signup` - 관리자 회원가입
- `POST /manager/login` - 관리자 로그인
- `GET /manager/me` - 관리자 정보 조회 🔒

### 사용자 (User)
- `POST /user/login` - 사용자 로그인
- `PUT /user/first-login` - 첫 로그인 정보 입력 🔒
- `GET /user/me` - 사용자 정보 조회 🔒
- `PUT /user/me` - 사용자 정보 수정 🔒
- `PUT /user/change-password` - 비밀번호 변경 🔒

### 계정 관리 (관리자 전용)
- `GET /accounts/users` - 사용자 목록 조회 🔒👑
- `GET /accounts/users/{user_id}` - 사용자 상세 조회 🔒👑
- `POST /accounts/users` - 사용자 계정 생성 🔒👑
- `PUT /accounts/users/{user_id}` - 사용자 정보 수정 🔒👑
- `DELETE /accounts/users/{user_id}` - 사용자 삭제 🔒👑

### 기간제 인력
- `GET /term-employees/search` - 이름/생년월일로 검색 🔒
- `GET /term-employees` - 목록 조회 🔒
- `GET /term-employees/{employee_id}` - 상세 조회 🔒
- `POST /term-employees` - 인력 등록 🔒
- `PUT /term-employees/{employee_id}` - 정보 수정 🔒
- `DELETE /term-employees/{employee_id}` - 삭제 🔒

### 부서
- `GET /departments` - 부서 목록 조회
- `GET /departments/{department_id}` - 부서 상세 조회
- `POST /departments` - 부서 생성 🔒👑
- `PUT /departments/{department_id}` - 부서 수정 🔒👑
- `DELETE /departments/{department_id}` - 부서 삭제 🔒👑

### OAuth 인증
- `GET /auth/google` - Google OAuth 로그인 시작
- `GET /auth/google/callback` - Google OAuth 콜백
- `GET /auth/apple` - Apple OAuth 로그인 시작
- `POST /auth/apple/callback` - Apple OAuth 콜백
- `GET /auth/naver` - Naver OAuth 로그인 시작
- `GET /auth/naver/callback` - Naver OAuth 콜백
- `GET /auth/kakao` - Kakao OAuth 로그인 시작
- `GET /auth/kakao/callback` - Kakao OAuth 콜백
- `GET /auth/me` - 현재 사용자 정보 조회 🔒
- `PUT /auth/me` - 사용자 정보 수정 🔒
- `POST /auth/logout` - 로그아웃 🔒
- `POST /auth/refresh` - 액세스 토큰 갱신

### 게시글
- `POST /posts` - 게시글 작성 🔒
- `GET /posts` - 게시글 목록 조회
- `GET /posts/me` - 내가 작성한 게시글 조회 🔒
- `GET /posts/{post_id}` - 게시글 상세 조회
- `PUT /posts/{post_id}` - 게시글 수정 🔒
- `DELETE /posts/{post_id}` - 게시글 삭제 🔒

🔒 = 인증 필요 | 👑 = 관리자 전용

## 📁 프로젝트 구조

```
FestAPI/
├── alembic/              # 데이터베이스 마이그레이션
│   ├── versions/         # 마이그레이션 버전 파일
│   └── env.py           # Alembic 환경 설정
├── app/
│   ├── core/            # 설정 및 공통 기능
│   │   ├── config.py    # 환경 설정
│   │   ├── database.py  # DB 설정
│   │   └── exceptions.py
│   ├── db/              # 데이터베이스
│   │   ├── models/      # SQLAlchemy 모델
│   │   │   ├── manager.py
│   │   │   ├── user.py
│   │   │   ├── department.py
│   │   │   └── term_employee.py
│   │   ├── base.py
│   │   └── session.py
│   ├── schemas/         # Pydantic 스키마
│   │   ├── manager.py
│   │   ├── user_auth.py
│   │   ├── department.py
│   │   └── term_employee.py
│   ├── services/        # 비즈니스 로직
│   │   ├── password_service.py
│   │   ├── manager_service.py
│   │   └── user_service.py
│   ├── routers/         # API 엔드포인트
│   │   ├── manager.py
│   │   ├── user.py
│   │   ├── account.py
│   │   ├── department.py
│   │   └── term_employee.py
│   ├── middleware/      # 미들웨어
│   └── main.py          # FastAPI 앱
├── tests/               # 테스트
├── .env.example         # 환경 변수 예시
├── alembic.ini          # Alembic 설정
├── Dockerfile
├── docker-compose.yml
├── requirements.txt     # 기본 의존성
├── requirements-dev.txt # 개발 의존성
└── requirements-prod.txt# 프로덕션 의존성
```

## 🔧 주요 기능 설명

### 1. 이중 인증 시스템

시스템은 관리자와 사용자로 역할이 분리되어 있습니다.

- **관리자 (Manager)**: 사용자 계정 관리, 부서 관리 권한
- **사용자 (User)**: 기간제 인력 정보 조회 및 관리

### 2. 첫 로그인 플로우

1. 관리자가 사용자 계정 생성 (username + 임시 비밀번호)
2. 사용자가 임시 비밀번호로 로그인
3. `is_first_login: true` 응답 확인
4. `/user/first-login` 엔드포인트로 담당자 정보 및 새 비밀번호 입력
5. `is_first_login: false`로 변경되어 정상 사용

### 3. 기간제 인력 검색

- **이름 검색 (필수)**: 부분 일치 검색
- **생년월일 (선택)**: 정확한 날짜 일치

### 4. 비밀번호 정책

- 8자 이상 30자 이하
- bcrypt 해싱 저장

## 🧪 테스트

```bash
# 전체 테스트 실행
pytest tests/ -v

# 커버리지 포함
pytest tests/ --cov=app --cov-report=html

# 특정 테스트 파일만 실행
pytest tests/test_manager.py -v
```

## 🔒 보안

- JWT 기반 인증 (Access + Refresh Token)
- 역할 기반 접근 제어 (Manager/User)
- bcrypt 비밀번호 해싱
- 환경 변수로 민감 정보 관리
- SQL Injection 방지 (SQLAlchemy ORM)

## 🐛 트러블슈팅

### 데이터베이스 연결 오류

```bash
# PostgreSQL 실행 확인
psql -U postgres -c "SELECT 1"

# DATABASE_URL 확인
echo $DATABASE_URL
```

### 마이그레이션 오류

```bash
# 마이그레이션 상태 확인
alembic current

# 마이그레이션 롤백
alembic downgrade -1

# 처음부터 다시
alembic downgrade base
alembic upgrade head
```

### 패키지 설치 오류 (asyncpg, psycopg2)

```bash
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql-dev python3-dev

# 그 후 다시 설치
pip install asyncpg psycopg2-binary
```

## 🛠️ 개발 환경 설정

### VS Code 사용자

1. **Python 인터프리터 선택**
   - `Cmd/Ctrl + Shift + P` → "Python: Select Interpreter"
   - `./venv/bin/python` 선택

2. **권장 설정** (`.vscode/settings.json` 생성)
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.analysis.typeCheckingMode": "basic",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "sonarlint.rules": {
    "python:S1192": {
      "level": "off"
    }
  }
}
```

**참고**: SonarLint의 S1192 규칙(문자열 중복)은 이미 상수화된 코드에서도 경고를 표시할 수 있습니다. 위 설정으로 비활성화할 수 있습니다.

3. **권장 확장 프로그램**
   - Python (Microsoft)
   - Pylance (Microsoft)
   - Black Formatter (Microsoft)

### 타입 체킹

프로젝트에 `pyrightconfig.json`이 포함되어 있어 SQLAlchemy 관련 타입 체킹 오류가 자동으로 무시됩니다.

## 📝 개발 가이드

### 새로운 모델 추가

1. `app/db/models/`에 모델 파일 생성
2. `app/db/models/__init__.py`에 import 추가
3. 마이그레이션 생성: `alembic revision --autogenerate -m "Add new model"`
4. 마이그레이션 실행: `alembic upgrade head`

### 새로운 엔드포인트 추가

1. `app/schemas/`에 Pydantic 스키마 정의
2. `app/routers/`에 라우터 생성
3. `app/main.py`에 라우터 등록

## 🎨 코드 품질

### 메시지 상수화

프로젝트 전반에 걸쳐 하드코딩된 에러/성공 메시지를 상수로 관리합니다.

- **위치**: `app/core/messages.py`
- **클래스**:
  - `ErrorMessages`: 모든 에러 메시지 상수
  - `SuccessMessages`: 성공 메시지 상수

**적용 범위**:
- ✅ 라우터 (routers/)
- ✅ 서비스 (services/)
- ✅ Pydantic 스키마 (schemas/)

**장점**:
- 중복 문자열 제거로 유지보수성 향상
- 일관된 메시지 관리
- SonarLint 코드 품질 규칙 준수

## 👨‍💻 Author

FestAPI Team
