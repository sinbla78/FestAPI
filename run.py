import uvicorn
from app.core.config import settings

def print_oauth_setup_guide():
    """OAuth 설정 가이드 출력"""
    print("🚀 OAuth 인증 API 서버를 시작합니다...")
    print()
    print("📝 OAuth 설정 가이드:")
    print()
    
    # Google OAuth 설정
    print("🔵 Google OAuth 설정:")
    print("   1. Google Cloud Console (https://console.cloud.google.com) 접속")
    print("   2. 새 프로젝트 생성 또는 기존 프로젝트 선택")
    print("   3. 'API 및 서비스' > '사용자 인증 정보' 메뉴")
    print("   4. '사용자 인증 정보 만들기' > 'OAuth 2.0 클라이언트 ID'")
    print("   5. 애플리케이션 유형: '웹 애플리케이션'")
    print("   6. 승인된 리디렉션 URI: http://localhost:8000/auth/google/callback")
    print()
    
    # Apple OAuth 설정  
    print("🍎 Apple OAuth 설정:")
    print("   1. Apple Developer Program 가입 ($99/년)")
    print("   2. developer.apple.com > Certificates, Identifiers & Profiles")
    print("   3. Keys > 새 키 생성 > 'Sign in with Apple' 체크")
    print("   4. .p8 파일 다운로드 (한번만 가능!)")
    print("   5. Identifiers > Service IDs 생성")
    print("   6. 'Sign in with Apple' 설정")
    print("   7. Return URLs: http://localhost:8000/auth/apple/callback")
    print()
    
    # .env 파일 설정
    print("📄 .env 파일 설정 예시:")
    print("   # Google OAuth")
    print("   GOOGLE_CLIENT_ID=your-google-client-id")
    print("   GOOGLE_CLIENT_SECRET=your-google-client-secret")
    print()
    print("   # Apple OAuth")  
    print("   APPLE_CLIENT_ID=com.yourcompany.yourapp.signin")
    print("   APPLE_TEAM_ID=XXXXXXXXXX")
    print("   APPLE_KEY_ID=XXXXXXXXXX")
    print("   APPLE_PRIVATE_KEY_PATH=./AuthKey_XXXXXXXXXX.p8")
    print()
    print("   # JWT 설정")
    print("   JWT_SECRET_KEY=your-super-secret-jwt-key")
    print()
    
    # 현재 설정 상태 확인
    print("🔍 현재 설정 상태:")
    google_configured = bool(settings.google_client_id and settings.google_client_secret)
    apple_configured = bool(settings.apple_client_id and settings.apple_team_id and 
                           settings.apple_key_id and settings.apple_private_key_path)
    
    print(f"   Google OAuth: {'✅ 설정됨' if google_configured else '❌ 미설정'}")
    print(f"   Apple OAuth:  {'✅ 설정됨' if apple_configured else '❌ 미설정'}")
    
    if not google_configured and not apple_configured:
        print("   ⚠️  OAuth 설정이 필요합니다!")
        print("   💡 테스트만 하려면 /docs에서 API 문서를 확인하세요.")
    elif google_configured and not apple_configured:
        print("   💡 Google 로그인만 사용 가능합니다.")
    elif apple_configured and not google_configured:
        print("   💡 Apple 로그인만 사용 가능합니다.")
    else:
        print("   🎉 모든 OAuth 제공자 설정 완료!")
    
    print()
    print("🌐 서버 정보:")
    print(f"   홈페이지:     http://localhost:8000")
    print(f"   API 문서:     http://localhost:8000/docs")
    print(f"   헬스체크:     http://localhost:8000/health")
    print(f"   Google 로그인: http://localhost:8000/auth/google")
    print(f"   Apple 로그인:  http://localhost:8000/auth/apple")
    print()

if __name__ == "__main__":
    print_oauth_setup_guide()

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )