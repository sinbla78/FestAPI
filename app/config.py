from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # JWT 설정
    jwt_secret_key: str = "your-secret-key-here"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # Google OAuth
    google_client_id: str
    google_client_secret: str
    redirect_uri_google: str
    google_oauth_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    google_token_url: str = "https://oauth2.googleapis.com/token"
    google_user_info_url: str = "https://www.googleapis.com/oauth2/v2/userinfo"

    # Apple OAuth
    apple_client_id: str
    apple_team_id: str
    apple_key_id: str
    apple_private_key_path: str = "./apple_private_key.p8"
    redirect_uri_apple: str
    apple_oauth_url: str = "https://appleid.apple.com/auth/authorize"
    apple_token_url: str = "https://appleid.apple.com/auth/token"
    apple_keys_url: str = "https://appleid.apple.com/auth/keys"

    # Naver OAuth
    naver_client_id: str
    naver_client_secret: str
    redirect_uri_naver: str
    naver_oauth_url: str = "https://nid.naver.com/oauth2.0/authorize"
    naver_token_url: str = "https://nid.naver.com/oauth2.0/token"
    naver_user_info_url: str = "https://openapi.naver.com/v1/nid/me"

    # Kakao OAuth
    kakao_client_id: str
    kakao_client_secret: str
    redirect_uri_kakao: str
    kakao_oauth_url: str = "https://kauth.kakao.com/oauth/authorize"
    kakao_token_url: str = "https://kauth.kakao.com/oauth/token"
    kakao_user_info_url: str = "https://kapi.kakao.com/v2/user/me"
    kakao_logout_url: str = "https://kapi.kakao.com/v1/user/logout"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
