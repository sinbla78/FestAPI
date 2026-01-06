from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


class OAuthProvider(str, Enum):
    """OAuth 제공자"""
    GOOGLE = "google"
    APPLE = "apple"
    NAVER = "naver"
    KAKAO = "kakao"


class User(BaseModel):
    """사용자 모델"""
    id: str
    email: EmailStr
    name: str
    picture: Optional[str] = None
    verified_email: bool = False
    provider: OAuthProvider
    provider_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class UserResponse(BaseModel):
    """사용자 응답 (토큰 포함)"""
    user: User
    access_token: str
