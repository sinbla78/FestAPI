from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

class OAuthProvider(str, Enum):
    GOOGLE = "google"
    APPLE = "apple"
    NAVER = "naver"
    KAKAO = "kakao"

class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    picture: Optional[str] = None
    verified_email: bool = False
    provider: OAuthProvider
    provider_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    picture: Optional[str] = None

class UserResponse(BaseModel):
    user: User
    access_token: str