import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"🚀 {settings.app_name} v{settings.app_version} 서버를 시작합니다...")
    print("📝 설정 전 필요사항:")
    print("   1. Google Cloud Console에서 OAuth 2.0 클라이언트 ID 생성")
    print("   2. 승인된 리디렉션 URI에 http://localhost:8000/auth/google/callback 추가")
    print("   3. .env 파일에 Google OAuth 정보 설정")
    print("🌐 서버 주소: http://localhost:8000")
    print("📖 API 문서: http://localhost:8000/docs")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )