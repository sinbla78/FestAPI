import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Google OAuth 설정
    google_client_id: str
    google_client_secret: str
    redirect_uri: str = "http://localhost:8000/auth/google/callback"
    
    # JWT 설정
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # 앱 설정
    app_name: str = "Google OAuth 인증 서비스"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Google OAuth URLs
    google_oauth_url: str = "https://accounts.google.com/o/oauth2/auth"
    google_token_url: str = "https://oauth2.googleapis.com/token"
    google_user_info_url: str = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    class Config:
        env_file = ".env"

settings = Settings()