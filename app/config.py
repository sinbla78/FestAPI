import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Google OAuth 설정
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    redirect_uri_google: str = os.getenv("REDIRECT_URI_GOOGLE", "http://localhost:8000/auth/google/callback")
    
    # Apple OAuth 설정
    apple_client_id: str = os.getenv("APPLE_CLIENT_ID", "")  # Service ID
    apple_team_id: str = os.getenv("APPLE_TEAM_ID", "")
    apple_key_id: str = os.getenv("APPLE_KEY_ID", "")
    apple_private_key_path: str = os.getenv("APPLE_PRIVATE_KEY_PATH", "")
    redirect_uri_apple: str = os.getenv("REDIRECT_URI_APPLE", "http://localhost:8000/auth/apple/callback")
    
    # JWT 설정
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-this-in-production")
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # 앱 설정
    app_name: str = "Multi OAuth 인증 서비스"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Google OAuth URLs
    google_oauth_url: str = "https://accounts.google.com/o/oauth2/auth"
    google_token_url: str = "https://oauth2.googleapis.com/token"
    google_user_info_url: str = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    # Apple OAuth URLs
    apple_oauth_url: str = "https://appleid.apple.com/auth/authorize"
    apple_token_url: str = "https://appleid.apple.com/auth/token"
    apple_keys_url: str = "https://appleid.apple.com/auth/keys"

settings = Settings()