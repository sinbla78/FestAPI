import jwt
import httpx
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from urllib.parse import urlencode

from app.config import settings
from app.models import User, GoogleUserInfo, OAuthProvider
from app.database import db
from app.apple_auth import AppleAuthService

security = HTTPBearer()

class AuthService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        try:
            payload = jwt.decode(
                credentials.credentials, 
                settings.jwt_secret_key, 
                algorithms=[settings.jwt_algorithm]
            )
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return email
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def get_current_user(email: str = Depends(verify_token)) -> User:
        user = db.get_user_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    # Google OAuth 메서드들
    @staticmethod
    def get_google_auth_url() -> str:
        params = {
            "client_id": settings.google_client_id,
            "redirect_uri": settings.redirect_uri_google,
            "scope": "openid email profile",
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent"
        }
        return f"{settings.google_oauth_url}?{urlencode(params)}"
    
    @staticmethod
    async def get_google_user_info(code: str) -> GoogleUserInfo:
        try:
            token_data = {
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.redirect_uri_google,
                "grant_type": "authorization_code",
                "code": code
            }
            
            async with httpx.AsyncClient() as client:
                token_response = await client.post(settings.google_token_url, data=token_data)
                token_response.raise_for_status()
                tokens = token_response.json()
                
                headers = {"Authorization": f"Bearer {tokens['access_token']}"}
                user_response = await client.get(settings.google_user_info_url, headers=headers)
                user_response.raise_for_status()
                user_info = user_response.json()
            
            return GoogleUserInfo(**user_info)
            
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Google OAuth 인증 실패: {str(e)}"
            )