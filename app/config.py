from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 기본 설정
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    
    # Apple OAuth
    APPLE_CLIENT_ID: str
    APPLE_TEAM_ID: str
    APPLE_KEY_ID: str
    APPLE_PRIVATE_KEY: str
    APPLE_REDIRECT_URI: str
    
    # Naver OAuth
    NAVER_CLIENT_ID: str
    NAVER_CLIENT_SECRET: str
    NAVER_REDIRECT_URI: str
    
    # Kakao OAuth
    KAKAO_CLIENT_ID: str
    KAKAO_CLIENT_SECRET: str
    KAKAO_REDIRECT_URI: str
    
    class Config:
        env_file = ".env"

settings = Settings()