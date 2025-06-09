from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class OAuthProvider(str, Enum):
    GOOGLE = "google"
    APPLE = "apple"

class User(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    verified_email: bool = False
    provider: OAuthProvider
    provider_id: str  # 구글 ID 또는 애플 ID
    created_at: datetime = None
    updated_at: datetime = None
    
    def __init__(self, **data):
        if 'created_at' not in data:
            data['created_at'] = datetime.utcnow()
        if 'updated_at' not in data:
            data['updated_at'] = datetime.utcnow()
        super().__init__(**data)

class UserCreate(BaseModel):
    email: str
    name: str
    picture: Optional[str] = None
    provider: OAuthProvider
    provider_id: str

class UserUpdate(BaseModel):
    name: Optional[str] = None

class UserResponse(BaseModel):
    user: User
    access_token: str
    token_type: str = "bearer"

class GoogleUserInfo(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    verified_email: bool = False

class AppleUserInfo(BaseModel):
    sub: str  # Apple의 사용자 ID
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None