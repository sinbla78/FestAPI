from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, EmailStr, Field, field_validator, HttpUrl

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
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="변경할 사용자 이름",
        examples=["김철수"]
    )
    picture: Optional[str] = Field(
        None,
        description="변경할 프로필 이미지 URL",
        examples=["https://example.com/new-avatar.jpg"]
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """이름 검증 - 공백만 있는 문자열 방지"""
        if v is not None:
            if not v.strip():
                raise ValueError("이름은 공백만 입력할 수 없습니다.")
            return v.strip()
        return v

    @field_validator("picture")
    @classmethod
    def validate_picture_url(cls, v: Optional[str]) -> Optional[str]:
        """프로필 이미지 URL 검증"""
        if v is not None:
            if not v.strip():
                raise ValueError("URL은 공백만 입력할 수 없습니다.")
            # 기본적인 URL 형식 검증
            if not v.startswith(("http://", "https://")):
                raise ValueError("올바른 URL 형식이 아닙니다. (http:// 또는 https://로 시작해야 합니다)")
            return v.strip()
        return v

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
