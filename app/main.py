from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, users, protected
from app.database import db

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Google OAuth를 사용한 사용자 인증 및 관리 시스템"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(protected.router)

# 기본 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "message": "Google OAuth 인증 서비스",
        "version": settings.app_version,
        "endpoints": {
            "login": "/auth/google",
            "callback": "/auth/google/callback",
            "profile": "/auth/me",
            "users": "/users",
            "logout": "/auth/logout",
            "protected": "/protected"
        }
    }