import httpx
import secrets
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from urllib.parse import urlencode

from app.core.config import settings
from app.schemas.auth import NaverUserInfo


class NaverAuthService:
    """네이버 OAuth 인증 서비스"""

    @staticmethod
    def get_auth_url(state: Optional[str] = None) -> str:
        """네이버 로그인 URL 생성"""
        # state 파라미터가 없으면 랜덤 생성 (CSRF 공격 방지)
        if not state:
            state = secrets.token_urlsafe(32)

        params = {
            "response_type": "code",
            "client_id": settings.naver_client_id,
            "redirect_uri": settings.redirect_uri_naver,
            "state": state
        }

        return f"{settings.naver_oauth_url}?{urlencode(params)}"

    @staticmethod
    async def get_tokens(code: str, state: str) -> Dict[str, Any]:
        """네이버 서버에서 토큰 받기"""
        try:
            token_data = {
                "grant_type": "authorization_code",
                "client_id": settings.naver_client_id,
                "client_secret": settings.naver_client_secret,
                "code": code,
                "state": state
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.naver_token_url,
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get Naver tokens: {str(e)}"
            )

    @staticmethod
    async def get_user_info(access_token: str) -> NaverUserInfo:
        """네이버 사용자 정보 가져오기"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    settings.naver_user_info_url,
                    headers=headers
                )
                response.raise_for_status()
                user_data = response.json()

                # 네이버 API 응답 구조 확인
                if user_data.get("resultcode") != "00":
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Naver API Error: {user_data.get('message', 'Unknown error')}"
                    )

                # 네이버 사용자 정보 파싱
                response_data = user_data.get("response", {})

                return NaverUserInfo(
                    id=response_data.get("id"),
                    email=response_data.get("email"),
                    name=response_data.get("name"),
                    nickname=response_data.get("nickname"),
                    profile_image=response_data.get("profile_image"),
                    age=response_data.get("age"),
                    gender=response_data.get("gender"),
                    birthday=response_data.get("birthday"),
                    birthyear=response_data.get("birthyear"),
                    mobile=response_data.get("mobile")
                )

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get Naver user info: {str(e)}"
            )

    @staticmethod
    async def revoke_token(access_token: str) -> bool:
        """네이버 토큰 무효화"""
        try:
            params = {
                "grant_type": "delete",
                "client_id": settings.naver_client_id,
                "client_secret": settings.naver_client_secret,
                "access_token": access_token,
                "service_provider": "NAVER"
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.naver_token_url,
                    data=params,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                result = response.json()

                return result.get("result") == "success"

        except httpx.HTTPError:
            return False

    @staticmethod
    def generate_state() -> str:
        """CSRF 방지용 state 파라미터 생성"""
        return secrets.token_urlsafe(32)
