import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from urllib.parse import urlencode

from app.config import settings
from app.schemas.auth import KakaoUserInfo


class KakaoAuthService:
    """카카오 OAuth 인증 서비스"""

    @staticmethod
    def get_auth_url(state: Optional[str] = None) -> str:
        """카카오 로그인 URL 생성"""
        params = {
            "client_id": settings.kakao_client_id,
            "redirect_uri": settings.redirect_uri_kakao,
            "response_type": "code",
            "scope": "profile_nickname,profile_image,account_email"
        }

        if state:
            params["state"] = state

        return f"{settings.kakao_oauth_url}?{urlencode(params)}"

    @staticmethod
    async def get_tokens(code: str) -> Dict[str, Any]:
        """카카오 서버에서 토큰 받기"""
        try:
            token_data = {
                "grant_type": "authorization_code",
                "client_id": settings.kakao_client_id,
                "client_secret": settings.kakao_client_secret,
                "redirect_uri": settings.redirect_uri_kakao,
                "code": code
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.kakao_token_url,
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get Kakao tokens: {str(e)}"
            )

    @staticmethod
    async def get_user_info(access_token: str) -> KakaoUserInfo:
        """카카오 사용자 정보 가져오기"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    settings.kakao_user_info_url,
                    headers=headers
                )
                response.raise_for_status()
                user_data = response.json()

                # 카카오 API 응답 구조에 맞게 파싱
                kakao_account = user_data.get("kakao_account", {})
                profile = kakao_account.get("profile", {})

                return KakaoUserInfo(
                    id=str(user_data.get("id")),
                    email=kakao_account.get("email"),
                    email_verified=kakao_account.get("is_email_verified", False),
                    nickname=profile.get("nickname"),
                    profile_image=profile.get("profile_image_url"),
                    profile_image_url=profile.get("profile_image_url"),
                    thumbnail_image=profile.get("thumbnail_image_url"),
                    thumbnail_image_url=profile.get("thumbnail_image_url")
                )

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get Kakao user info: {str(e)}"
            )

    @staticmethod
    async def revoke_token(access_token: str) -> bool:
        """카카오 토큰 무효화 (로그아웃)"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.kakao_logout_url,
                    headers=headers
                )
                response.raise_for_status()
                return True

        except httpx.HTTPError:
            return False
