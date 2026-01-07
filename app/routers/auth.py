from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from typing import Optional

from app.services import AuthService, GoogleAuthService, AppleAuthService, NaverAuthService, KakaoAuthService
from app.services.auth_service import security
from app.models import User, OAuthProvider, UserResponse, TokenResponse
from app.schemas import UserUpdate
from app.core.database import db
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["인증"])

# Google OAuth
@router.get(
    "/google",
    summary="Google OAuth 로그인",
    description="""
    Google OAuth 2.0 인증을 시작합니다.

    이 엔드포인트는 Google 로그인 페이지로 리디렉션합니다.
    사용자가 Google에서 인증을 완료하면 `/auth/google/callback`으로 돌아옵니다.
    """,
    response_class=RedirectResponse,
)
async def google_login():
    """Google OAuth 로그인 시작"""
    google_auth_url = GoogleAuthService.get_auth_url()
    return RedirectResponse(url=google_auth_url)

@router.get(
    "/google/callback",
    summary="Google OAuth 콜백",
    description="""
    Google OAuth 인증 완료 후 호출되는 콜백 엔드포인트입니다.

    - 사용자 정보를 Google에서 가져옵니다
    - 신규 사용자인 경우 자동으로 회원가입합니다
    - JWT 액세스 토큰을 생성하여 반환합니다
    """,
    response_model=UserResponse,
    responses={
        200: {
            "description": "로그인 성공",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": "google_123456789",
                            "email": "user@gmail.com",
                            "name": "홍길동",
                            "picture": "https://lh3.googleusercontent.com/a/default-user",
                            "verified_email": True,
                            "provider": "google",
                            "provider_id": "123456789"
                        },
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    }
                }
            }
        },
        400: {"description": "OAuth 인증 실패"}
    }
)
async def google_callback(code: str) -> UserResponse:
    """Google OAuth 콜백 처리"""
    google_user = await GoogleAuthService.get_user_info(code)
    
    user = db.get_user_by_email(google_user.email)
    if not user:
        user_data = {
            "id": f"google_{google_user.id}",
            "email": google_user.email,
            "name": google_user.name,
            "picture": google_user.picture,
            "verified_email": google_user.verified_email,
            "provider": OAuthProvider.GOOGLE,
            "provider_id": google_user.id
        }
        user = db.create_user(user_data)

    # 액세스 토큰 + 리프레시 토큰 생성
    tokens = AuthService.create_tokens(user.email)
    db.add_session(tokens["access_token"], user.email)

    return UserResponse(
        user=user,
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"]
    )

# Apple OAuth
@router.get("/apple")
async def apple_login():
    """Apple OAuth 로그인 시작"""
    apple_auth_url = AppleAuthService.get_auth_url()
    return RedirectResponse(url=apple_auth_url)

@router.post("/apple/callback")
async def apple_callback(
    code: str = Form(...),
    id_token: Optional[str] = Form(None),
    user: Optional[str] = Form(None),
    state: Optional[str] = Form(None)
) -> UserResponse:
    """Apple OAuth 콜백 처리 (POST 방식)"""
    try:
        tokens = await AppleAuthService.get_tokens(code)
        apple_user = await AppleAuthService.verify_token(tokens["id_token"])
        
        user_name = apple_user.name
        if user and not user_name:
            try:
                import json
                user_data = json.loads(user)
                if user_data.get("name"):
                    first_name = user_data["name"].get("firstName", "")
                    last_name = user_data["name"].get("lastName", "")
                    user_name = f"{first_name} {last_name}".strip()
            except:
                user_name = "Apple User"
        
        if not user_name:
            user_name = "Apple User"
        
        email = apple_user.email or f"{apple_user.sub}@privaterelay.appleid.com"
        existing_user = db.get_user_by_email(email)
        
        if not existing_user:
            user_data = {
                "id": f"apple_{apple_user.sub}",
                "email": email,
                "name": user_name,
                "picture": None,
                "verified_email": apple_user.email_verified or False,
                "provider": OAuthProvider.APPLE,
                "provider_id": apple_user.sub
            }
            existing_user = db.create_user(user_data)
        
        tokens = AuthService.create_tokens(existing_user.email)
        db.add_session(tokens["access_token"], existing_user.email)
        
        return UserResponse(user=existing_user, access_token=tokens["access_token"], refresh_token=tokens["refresh_token"], token_type=tokens["token_type"])
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Apple OAuth 인증 실패: {str(e)}"
        )

# 네이버 OAuth
@router.get("/naver")
async def naver_login():
    """네이버 OAuth 로그인 시작"""
    naver_auth_url = NaverAuthService.get_auth_url()
    return RedirectResponse(url=naver_auth_url)

@router.get("/naver/callback")
async def naver_callback(code: str, state: str) -> UserResponse:
    """네이버 OAuth 콜백 처리"""
    try:
        tokens = await NaverAuthService.get_tokens(code, state)
        naver_user = await NaverAuthService.get_user_info(tokens["access_token"])
        
        user = db.get_user_by_email(naver_user.email)
        if not user:
            user_data = {
                "id": f"naver_{naver_user.id}",
                "email": naver_user.email,
                "name": naver_user.name,
                "picture": naver_user.profile_image,
                "verified_email": True,
                "provider": OAuthProvider.NAVER,
                "provider_id": naver_user.id
            }
            user = db.create_user(user_data)
        
        tokens = AuthService.create_tokens(user.email)
        db.add_session(tokens["access_token"], user.email)
        
        return UserResponse(user=user, access_token=tokens["access_token"], refresh_token=tokens["refresh_token"], token_type=tokens["token_type"])
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"네이버 OAuth 인증 실패: {str(e)}"
        )

# 카카오 OAuth
@router.get("/kakao")
async def kakao_login():
    """카카오 OAuth 로그인 시작"""
    kakao_auth_url = KakaoAuthService.get_auth_url()
    return RedirectResponse(url=kakao_auth_url)

@router.get("/kakao/callback")
async def kakao_callback(code: str) -> UserResponse:
    """카카오 OAuth 콜백 처리"""
    try:
        tokens = await KakaoAuthService.get_tokens(code)
        kakao_user = await KakaoAuthService.get_user_info(tokens["access_token"])
        
        email = kakao_user.email
        if not email:
            email = f"kakao_{kakao_user.id}@kakao.local"
        
        user = db.get_user_by_email(email)
        if not user:
            user_data = {
                "id": f"kakao_{kakao_user.id}",
                "email": email,
                "name": kakao_user.nickname or "카카오 사용자",
                "picture": kakao_user.profile_image or kakao_user.profile_image_url,
                "verified_email": kakao_user.email_verified if kakao_user.email else False,
                "provider": OAuthProvider.KAKAO,
                "provider_id": str(kakao_user.id)
            }
            user = db.create_user(user_data)
        
        tokens = AuthService.create_tokens(user.email)
        db.add_session(tokens["access_token"], user.email)
        
        return UserResponse(user=user, access_token=tokens["access_token"], refresh_token=tokens["refresh_token"], token_type=tokens["token_type"])
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"카카오 OAuth 인증 실패: {str(e)}"
        )

# 공통 엔드포인트들
@router.get(
    "/me",
    response_model=User,
    summary="현재 사용자 정보 조회",
    description="""
    인증된 사용자의 프로필 정보를 조회합니다.

    **인증 필요**: Bearer 토큰을 헤더에 포함해야 합니다.
    """,
    responses={
        200: {"description": "사용자 정보 조회 성공"},
        401: {"description": "인증 실패"},
        404: {"description": "사용자를 찾을 수 없음"}
    }
)
async def get_current_user_profile(current_user: User = Depends(AuthService.get_current_user)):
    """현재 사용자 프로필 조회"""
    return current_user

@router.put(
    "/me",
    response_model=User,
    summary="현재 사용자 정보 수정",
    description="""
    인증된 사용자의 프로필 정보를 수정합니다.

    **인증 필요**: Bearer 토큰을 헤더에 포함해야 합니다.

    수정 가능한 필드:
    - name: 사용자 이름
    - picture: 프로필 이미지 URL
    """,
    responses={
        200: {"description": "사용자 정보 수정 성공"},
        401: {"description": "인증 실패"},
        404: {"description": "사용자를 찾을 수 없음"}
    }
)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(AuthService.get_current_user)
):
    """현재 사용자 정보 업데이트"""
    update_data = user_update.dict(exclude_unset=True)
    updated_user = db.update_user(current_user.email, update_data)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )

    return updated_user

@router.post(
    "/logout",
    summary="로그아웃",
    description="""
    현재 세션을 종료하고 로그아웃합니다.

    **인증 필요**: Bearer 토큰을 헤더에 포함해야 합니다.
    """,
    responses={
        200: {
            "description": "로그아웃 성공",
            "content": {
                "application/json": {
                    "example": {"message": "성공적으로 로그아웃되었습니다."}
                }
            }
        },
        401: {"description": "인증 실패"}
    }
)
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """로그아웃"""
    token = credentials.credentials
    db.remove_session(token)
    return {"message": "성공적으로 로그아웃되었습니다."}


# 리프레시 토큰 요청 스키마
class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="리프레시 토큰", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="액세스 토큰 갱신",
    description="""
    리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급받습니다.

    **사용 시나리오**:
    1. 액세스 토큰이 만료되었을 때
    2. 리프레시 토큰을 요청 본문에 포함하여 POST
    3. 새로운 액세스 토큰과 리프레시 토큰을 받음

    **토큰 만료 시간**:
    - 액세스 토큰: 24시간
    - 리프레시 토큰: 7일
    """,
    responses={
        200: {
            "description": "토큰 갱신 성공",
        },
        401: {"description": "리프레시 토큰이 유효하지 않거나 만료됨"}
    }
)
async def refresh_access_token(request: RefreshTokenRequest) -> TokenResponse:
    """리프레시 토큰으로 액세스 토큰 갱신"""
    email = AuthService.verify_refresh_token(request.refresh_token)
    user = db.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    tokens = AuthService.create_tokens(email)
    db.add_session(tokens["access_token"], email)
    return TokenResponse(**tokens)

