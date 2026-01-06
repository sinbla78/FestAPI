from typing import Optional
from pydantic import BaseModel, EmailStr


class GoogleUserInfo(BaseModel):
    """구글 OAuth 사용자 정보"""
    id: str
    email: EmailStr
    name: str
    picture: Optional[str] = None
    verified_email: bool = False


class AppleUserInfo(BaseModel):
    """애플 OAuth 사용자 정보"""
    sub: str
    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = False
    name: Optional[str] = None


class NaverUserInfo(BaseModel):
    """네이버 OAuth 사용자 정보"""
    id: str
    email: EmailStr
    name: str
    nickname: Optional[str] = None
    profile_image: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    birthyear: Optional[str] = None
    mobile: Optional[str] = None


class KakaoUserInfo(BaseModel):
    """카카오 OAuth 사용자 정보"""
    id: str
    email: Optional[EmailStr] = None
    email_verified: bool = False
    nickname: Optional[str] = None
    profile_image_url: Optional[str] = None
    profile_image: Optional[str] = None
    thumbnail_image: Optional[str] = None
    thumbnail_image_url: Optional[str] = None
