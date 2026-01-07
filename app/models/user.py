from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class OAuthProvider(str, Enum):
    """OAuth 제공자"""
    GOOGLE = "google"
    APPLE = "apple"
    NAVER = "naver"
    KAKAO = "kakao"


class User(BaseModel):
    """사용자 모델"""
    id: str = Field(..., description="사용자 고유 ID", example="google_123456789")
    email: EmailStr = Field(..., description="사용자 이메일", example="user@example.com")
    name: str = Field(..., description="사용자 이름", example="홍길동")
    picture: Optional[str] = Field(None, description="프로필 이미지 URL", example="https://example.com/avatar.jpg")
    verified_email: bool = Field(False, description="이메일 인증 여부")
    provider: OAuthProvider = Field(..., description="OAuth 제공자")
    provider_id: str = Field(..., description="제공자의 사용자 ID", example="123456789")
    created_at: Optional[str] = Field(None, description="생성 일시")
    updated_at: Optional[str] = Field(None, description="수정 일시")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "google_123456789",
                "email": "user@example.com",
                "name": "홍길동",
                "picture": "https://lh3.googleusercontent.com/a/default-user",
                "verified_email": True,
                "provider": "google",
                "provider_id": "123456789",
                "created_at": "2024-01-06T12:00:00Z",
                "updated_at": "2024-01-06T12:00:00Z"
            }
        }


class TokenResponse(BaseModel):
    """토큰 응답 (액세스 + 리프레시)"""
    access_token: str = Field(..., description="JWT 액세스 토큰 (짧은 만료 시간)", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    refresh_token: str = Field(..., description="JWT 리프레시 토큰 (긴 만료 시간)", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", description="토큰 타입")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzA0NTQwMDAwfQ...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3MDQ2MjY0MDB9...",
                "token_type": "bearer"
            }
        }


class UserResponse(BaseModel):
    """사용자 응답 (사용자 정보 + 토큰)"""
    user: User = Field(..., description="사용자 정보")
    access_token: str = Field(..., description="JWT 액세스 토큰", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    refresh_token: str = Field(..., description="JWT 리프레시 토큰", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", description="토큰 타입")

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "google_123456789",
                    "email": "user@example.com",
                    "name": "홍길동",
                    "picture": "https://lh3.googleusercontent.com/a/default-user",
                    "verified_email": True,
                    "provider": "google",
                    "provider_id": "123456789",
                    "created_at": "2024-01-06T12:00:00Z",
                    "updated_at": "2024-01-06T12:00:00Z"
                },
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzA0NTQwMDAwfQ...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3MDQ2MjY0MDB9...",
                "token_type": "bearer"
            }
        }
