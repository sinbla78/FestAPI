from fastapi import FastAPI
from app.routers import auth, users, protected

app = FastAPI(
    title="OAuth 인증 API",
    description="Google, Apple, Naver, Kakao OAuth 지원",
    version="1.0.0"
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(protected.router)


@app.get("/")
async def root():
    """루트 엔드포인트"""
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
