from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class ManagerBase(BaseModel):
    """관리자 기본 스키마"""
    username: str = Field(..., min_length=4, max_length=255, description="관리자 아이디")
    email: Optional[str] = Field(None, description="관리자 이메일")


class ManagerCreate(BaseModel):
    """관리자 회원가입 스키마"""
    username: str = Field(..., min_length=4, max_length=255, description="관리자 아이디")
    password: str = Field(..., min_length=8, max_length=30, description="관리자 비밀번호")
    email: Optional[str] = Field(None, description="관리자 이메일")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """비밀번호 검증"""
        if len(v) < 8 or len(v) > 30:
            raise ValueError("비밀번호는 8자~30자까지 작성할 수 있습니다.")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin123",
                "password": "password1234",
                "email": "admin@example.com"
            }
        }


class ManagerLogin(BaseModel):
    """관리자 로그인 스키마"""
    username: str = Field(..., description="관리자 아이디")
    password: str = Field(..., description="관리자 비밀번호")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin123",
                "password": "password1234"
            }
        }


class ManagerResponse(BaseModel):
    """관리자 응답 스키마"""
    manager_id: int
    username: str
    email: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ManagerTokenResponse(BaseModel):
    """관리자 토큰 응답 스키마"""
    manager: ManagerResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True
