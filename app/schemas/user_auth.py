from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class UserCreate(BaseModel):
    """사용자 계정 생성 스키마 (관리자용)"""
    username: str = Field(..., min_length=4, max_length=255, description="사용자 아이디")
    password: str = Field(..., min_length=8, max_length=30, description="최초 로그인용 비밀번호")

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
                "username": "user123",
                "password": "password1234"
            }
        }


class UserLogin(BaseModel):
    """사용자 로그인 스키마"""
    username: str = Field(..., description="사용자 아이디")
    password: str = Field(..., description="사용자 비밀번호")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user123",
                "password": "password1234"
            }
        }


class FirstLoginInfoUpdate(BaseModel):
    """첫 로그인 정보 입력 스키마"""
    manager_name: str = Field(..., min_length=1, max_length=255, description="담당자 이름")
    new_password: str = Field(..., min_length=8, max_length=30, description="새 비밀번호")
    manager_number: str = Field(..., min_length=1, max_length=20, description="담당자 연락처")
    department_id: int = Field(..., description="담당부서 ID")

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """비밀번호 검증"""
        if len(v) < 8 or len(v) > 30:
            raise ValueError("비밀번호는 8자~30자까지 작성할 수 있습니다.")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "manager_name": "홍길동",
                "new_password": "newpassword123",
                "manager_number": "010-1234-5678",
                "department_id": 1
            }
        }


class UserInfoUpdate(BaseModel):
    """사용자 개인정보 수정 스키마"""
    manager_name: Optional[str] = Field(None, min_length=1, max_length=255, description="담당자 이름")
    manager_number: Optional[str] = Field(None, min_length=1, max_length=20, description="담당자 연락처")
    department_id: Optional[int] = Field(None, description="담당부서 ID")

    class Config:
        json_schema_extra = {
            "example": {
                "manager_name": "홍길동",
                "manager_number": "010-1234-5678",
                "department_id": 1
            }
        }


class PasswordChange(BaseModel):
    """비밀번호 변경 스키마"""
    current_password: str = Field(..., description="현재 비밀번호")
    new_password: str = Field(..., min_length=8, max_length=30, description="새 비밀번호")
    new_password_confirm: str = Field(..., min_length=8, max_length=30, description="새 비밀번호 확인")

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        """새 비밀번호 검증"""
        if len(v) < 8 or len(v) > 30:
            raise ValueError("비밀번호는 8자~30자까지 작성할 수 있습니다.")
        return v

    @field_validator("new_password_confirm")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """비밀번호 확인 일치 검증"""
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("새 비밀번호와 새 비밀번호 확인이 일치하지 않습니다.")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "currentpassword123",
                "new_password": "newpassword123",
                "new_password_confirm": "newpassword123"
            }
        }


class UserResponse(BaseModel):
    """사용자 응답 스키마"""
    user_id: int
    username: str
    email: Optional[str]
    manager_name: Optional[str]
    manager_number: Optional[str]
    department_id: Optional[int]
    is_first_login: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserTokenResponse(BaseModel):
    """사용자 토큰 응답 스키마"""
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    is_first_login: bool  # 첫 로그인 여부 추가

    class Config:
        from_attributes = True
