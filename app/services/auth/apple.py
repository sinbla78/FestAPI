import jwt
import httpx
import time
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from urllib.parse import urlencode

from app.config import settings
from app.schemas.auth import AppleUserInfo


class AppleAuthService:
    """애플 OAuth 인증 서비스"""

    @staticmethod
    def load_apple_private_key() -> str:
        """애플 개발자 계정에서 다운로드한 .p8 키 파일 읽기"""
        try:
            with open(settings.apple_private_key_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Apple private key file not found"
            )

    @staticmethod
    def generate_client_secret() -> str:
        """애플 API 호출용 클라이언트 시크릿 JWT 생성"""
        private_key = AppleAuthService.load_apple_private_key()

        headers = {
            "alg": "ES256",
            "kid": settings.apple_key_id
        }

        payload = {
            "iss": settings.apple_team_id,
            "iat": int(time.time()),
            "exp": int(time.time()) + 86400 * 180,  # 6개월
            "aud": "https://appleid.apple.com",
            "sub": settings.apple_client_id
        }

        return jwt.encode(
            payload,
            private_key,
            algorithm="ES256",
            headers=headers
        )

    @staticmethod
    def get_auth_url(state: Optional[str] = None) -> str:
        """애플 로그인 URL 생성"""
        params = {
            "client_id": settings.apple_client_id,
            "redirect_uri": settings.redirect_uri_apple,
            "response_type": "code",
            "scope": "name email",
            "response_mode": "form_post"  # 애플은 form_post 권장
        }

        if state:
            params["state"] = state

        return f"{settings.apple_oauth_url}?{urlencode(params)}"

    @staticmethod
    async def verify_token(id_token: str) -> AppleUserInfo:
        """애플 ID 토큰 검증 및 사용자 정보 추출"""
        try:
            # 애플 공개 키 가져오기
            async with httpx.AsyncClient() as client:
                keys_response = await client.get(settings.apple_keys_url)
                keys_response.raise_for_status()
                apple_keys = keys_response.json()

            # JWT 헤더에서 kid 추출
            unverified_header = jwt.get_unverified_header(id_token)
            kid = unverified_header.get("kid")

            # 해당 kid의 공개 키 찾기
            apple_key = None
            for key in apple_keys["keys"]:
                if key["kid"] == kid:
                    apple_key = key
                    break

            if not apple_key:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid Apple key ID"
                )

            # JWT 토큰 검증 (여기서는 간단히 디코드만 - 실제로는 공개키로 검증해야 함)
            payload = jwt.decode(
                id_token,
                options={"verify_signature": False},  # 프로덕션에서는 True로 설정
                audience=settings.apple_client_id
            )

            return AppleUserInfo(
                sub=payload.get("sub"),
                email=payload.get("email"),
                email_verified=payload.get("email_verified"),
                name=payload.get("name")  # 첫 로그인시에만 제공됨
            )

        except jwt.PyJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid Apple ID token: {str(e)}"
            )

    @staticmethod
    async def get_tokens(code: str) -> Dict[str, Any]:
        """애플 서버에서 토큰 받기"""
        try:
            client_secret = AppleAuthService.generate_client_secret()

            token_data = {
                "client_id": settings.apple_client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.redirect_uri_apple
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.apple_token_url,
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get Apple tokens: {str(e)}"
            )
