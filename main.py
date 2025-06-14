from fastapi import FastAPI

app = FastAPI(
    title="OAuth 인증 API",
    description="Google, Apple, Naver, Kakao OAuth 지원",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "OAuth 인증 API 서버",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 테스트용 간단한 엔드포인트
@app.get("/test")
async def test():
    return {"message": "API가 정상적으로 작동합니다!"}
