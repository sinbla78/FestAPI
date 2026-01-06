from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, EmailStr, Field

if TYPE_CHECKING:
    from app.models import User


class UserBase(BaseModel):
    """사용자 기본 스키마"""
    email: EmailStr
    name: str


class UserCreate(UserBase):
    """사용자 생성 스키마"""
    picture: Optional[str] = None
    verified_email: bool = False


class UserUpdate(BaseModel):
    """사용자 업데이트 스키마"""
    name: Optional[str] = Field(None, description="변경할 사용자 이름", example="김철수")
    picture: Optional[str] = Field(None, description="변경할 프로필 이미지 URL", example="https://example.com/new-avatar.jpg")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "김철수",
                "picture": "https://example.com/new-avatar.jpg"
            }
        }


class UserResponse(BaseModel):
    """사용자 응답 스키마 (토큰 포함)"""
    user: "User"
    access_token: str

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    """DB에 저장된 사용자 스키마"""
    id: str
    picture: Optional[str] = None
    verified_email: bool
    provider: str
    provider_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
