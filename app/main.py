from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.routers import auth, users, protected, posts
from app.core.logging import logger

# API 메타데이터
tags_metadata = [
    {
        "name": "인증",
        "description": "OAuth 2.0 인증 관련 엔드포인트. Google, Apple, Naver, Kakao 로그인을 지원합니다.",
    },
    {
        "name": "사용자",
        "description": "사용자 정보 조회 및 관리. **인증 필요**",
    },
    {
        "name": "게시글",
        "description": "게시글 CRUD 기능. 작성, 조회, 수정, 삭제를 지원합니다.",
    },
    {
        "name": "보호된 엔드포인트",
        "description": "인증된 사용자만 접근 가능한 엔드포인트 예제. **인증 필요**",
    },
]

app = FastAPI(
    title="OAuth 인증 API",
    description="""
## FestAPI - OAuth 2.0 인증 서비스

다양한 OAuth 제공자를 통한 소셜 로그인을 지원하는 REST API 서버입니다.

### 지원하는 OAuth 제공자
* 🔵 **Google OAuth 2.0**
* 🍎 **Apple Sign In**
* 💚 **Naver OAuth**
* 💛 **Kakao OAuth**

### 주요 기능
* OAuth 2.0 소셜 로그인
* JWT 기반 인증 및 세션 관리
* 사용자 정보 조회 및 수정
* 보호된 리소스 접근 제어

### 인증 방법
1. OAuth 로그인 엔드포인트를 통해 로그인
2. 응답으로 받은 `access_token` 사용
3. 요청 헤더에 `Authorization: Bearer <access_token>` 포함

### 개발 정보
- **GitHub**: [FestAPI Repository](https://github.com/yourorg/festapi)
- **문의**: support@festapi.com
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "FestAPI Team",
        "email": "support@festapi.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(protected.router)


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    logger.info("FastAPI 애플리케이션이 시작되었습니다.")
    logger.info("OAuth 인증 서버 v1.0.0")


@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info("FastAPI 애플리케이션이 종료되었습니다.")


@app.get("/")
async def root():
    """루트 엔드포인트"""
    logger.info("루트 엔드포인트 호출")
    return {
        "message": "OAuth 인증 API 서버",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


@app.get("/test")
async def test():
    """테스트용 엔드포인트"""
    return {"message": "API가 정상적으로 작동합니다!"}
