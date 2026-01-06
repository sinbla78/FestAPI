"""
서버 실행 스크립트

사용법:
    python -m app
    또는
    python app/run.py
"""
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

    # Naver OAuth 설정
    print("💚 Naver OAuth 설정:")
    print("   1. 네이버 개발자센터 (https://developers.naver.com) 접속")
    print("   2. 애플리케이션 등록")
    print("   3. 콜백 URL: http://localhost:8000/auth/naver/callback")
    print()

    # Kakao OAuth 설정
    print("💛 Kakao OAuth 설정:")
    print("   1. 카카오 개발자센터 (https://developers.kakao.com) 접속")
    print("   2. 애플리케이션 추가")
    print("   3. Redirect URI: http://localhost:8000/auth/kakao/callback")
    print()

    # .env 파일 설정
    print("📄 .env 파일 설정:")
    print("   cp .env.example .env")
    print("   그 다음 .env 파일을 열어 실제 값을 입력하세요")
    print()

    # 현재 설정 상태 확인
    print("🔍 현재 설정 상태:")
    try:
        google_configured = bool(settings.google_client_id and settings.google_client_secret)
        apple_configured = bool(settings.apple_client_id and settings.apple_team_id and
                               settings.apple_key_id)
        naver_configured = bool(settings.naver_client_id and settings.naver_client_secret)
        kakao_configured = bool(settings.kakao_client_id and settings.kakao_client_secret)

        print(f"   Google OAuth: {'✅ 설정됨' if google_configured else '❌ 미설정'}")
        print(f"   Apple OAuth:  {'✅ 설정됨' if apple_configured else '❌ 미설정'}")
        print(f"   Naver OAuth:  {'✅ 설정됨' if naver_configured else '❌ 미설정'}")
        print(f"   Kakao OAuth:  {'✅ 설정됨' if kakao_configured else '❌ 미설정'}")

        configured_count = sum([google_configured, apple_configured, naver_configured, kakao_configured])

        if configured_count == 0:
            print("   ⚠️  OAuth 설정이 필요합니다!")
            print("   💡 .env 파일을 설정하거나 /docs에서 API 문서를 확인하세요.")
        elif configured_count == 4:
            print("   🎉 모든 OAuth 제공자 설정 완료!")
        else:
            print(f"   💡 {configured_count}/4개 OAuth 제공자 설정됨")
    except Exception as e:
        print(f"   ⚠️  설정 확인 중 오류: {e}")
        print("   💡 .env 파일을 확인하세요")

    print()
    print("🌐 서버 정보:")
    print(f"   홈페이지:      http://localhost:8000")
    print(f"   API 문서:      http://localhost:8000/docs")
    print(f"   헬스체크:      http://localhost:8000/health")
    print(f"   Google 로그인:  http://localhost:8000/auth/google")
    print(f"   Apple 로그인:   http://localhost:8000/auth/apple")
    print(f"   Naver 로그인:   http://localhost:8000/auth/naver")
    print(f"   Kakao 로그인:   http://localhost:8000/auth/kakao")
    print()


def main():
    """서버 실행 메인 함수"""
    print_oauth_setup_guide()

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
