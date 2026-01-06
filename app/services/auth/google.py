import httpx
from typing import Dict, Any
from fastapi import HTTPException, status
from urllib.parse import urlencode

from app.config import settings
from app.schemas.auth import GoogleUserInfo


class GoogleAuthService:
    """구글 OAuth 인증 서비스"""

    @staticmethod
    def get_auth_url() -> str:
        """구글 OAuth 인증 URL 생성"""
        params = {
            "client_id": settings.google_client_id,
            "redirect_uri": settings.redirect_uri_google,
            "scope": "openid email profile",
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent"
        }
        return f"{settings.google_oauth_url}?{urlencode(params)}"

    @staticmethod
    async def get_user_info(code: str) -> GoogleUserInfo:
        """구글 인증 코드로 사용자 정보 가져오기"""
        try:
            token_data = {
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.redirect_uri_google,
                "grant_type": "authorization_code",
                "code": code
            }

            async with httpx.AsyncClient() as client:
                # 토큰 가져오기
                token_response = await client.post(settings.google_token_url, data=token_data)
                token_response.raise_for_status()
                tokens = token_response.json()

                # 사용자 정보 가져오기
                headers = {"Authorization": f"Bearer {tokens['access_token']}"}
                user_response = await client.get(settings.google_user_info_url, headers=headers)
                user_response.raise_for_status()
                user_info = user_response.json()

            return GoogleUserInfo(**user_info)

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Google OAuth 인증 실패: {str(e)}"
            )
