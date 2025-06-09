from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    picture: Optional[str] = None
    verified_email: bool = False
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    picture: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None

class UserResponse(BaseModel):
    user: User
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    exp: Optional[datetime] = None

class GoogleUserInfo(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    verified_email: bool = False