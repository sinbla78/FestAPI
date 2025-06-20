from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from typing import Optional

from app.auth import AuthService, security
from app.apple_auth import AppleAuthService
from app.naver_auth import NaverAuthService
from app.kakao_auth import KakaoAuthService
from app.models import User, UserResponse, UserUpdate, OAuthProvider
from app.database import db

router = APIRouter(prefix="/auth", tags=["인증"])

# Google OAuth
@router.get("/google")
async def google_login():
    """Google OAuth 로그인 시작"""
    google_auth_url = AuthService.get_google_auth_url()
    return RedirectResponse(url=google_auth_url)

@router.get("/google/callback")
async def google_callback(code: str) -> UserResponse:
    """Google OAuth 콜백 처리"""
    google_user = await AuthService.get_google_user_info(code)
    
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
    
    access_token = AuthService.create_access_token(data={"sub": user.email})
    db.add_session(access_token, user.email)
    
    return UserResponse(user=user, access_token=access_token)

# Apple OAuth
@router.get("/apple")
async def apple_login():
    """Apple OAuth 로그인 시작"""
    apple_auth_url = AppleAuthService.get_apple_auth_url()
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
        tokens = await AppleAuthService.get_apple_tokens(code)
        apple_user = await AppleAuthService.verify_apple_token(tokens["id_token"])
        
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
        
        access_token = AuthService.create_access_token(data={"sub": existing_user.email})
        db.add_session(access_token, existing_user.email)
        
        return UserResponse(user=existing_user, access_token=access_token)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Apple OAuth 인증 실패: {str(e)}"
        )

# 네이버 OAuth
@router.get("/naver")
async def naver_login():
    """네이버 OAuth 로그인 시작"""
    naver_auth_url = NaverAuthService.get_naver_auth_url()
    return RedirectResponse(url=naver_auth_url)

@router.get("/naver/callback")
async def naver_callback(code: str, state: str) -> UserResponse:
    """네이버 OAuth 콜백 처리"""
    try:
        tokens = await NaverAuthService.get_naver_tokens(code, state)
        naver_user = await NaverAuthService.get_naver_user_info(tokens["access_token"])
        
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
        
        access_token = AuthService.create_access_token(data={"sub": user.email})
        db.add_session(access_token, user.email)
        
        return UserResponse(user=user, access_token=access_token)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"네이버 OAuth 인증 실패: {str(e)}"
        )

# 카카오 OAuth
@router.get("/kakao")
async def kakao_login():
    """카카오 OAuth 로그인 시작"""
    kakao_auth_url = KakaoAuthService.get_kakao_auth_url()
    return RedirectResponse(url=kakao_auth_url)

@router.get("/kakao/callback")
async def kakao_callback(code: str) -> UserResponse:
    """카카오 OAuth 콜백 처리"""
    try:
        tokens = await KakaoAuthService.get_kakao_tokens(code)
        kakao_user = await KakaoAuthService.get_kakao_user_info(tokens["access_token"])
        
        email = kakao_user.email
        if not email:
            email = f"kakao_{kakao_user.id}@kakao.local"
        
        user = db.get_user_by_email(email)
        if not user:
            user_data = {
                "id": f"kakao_{kakao_user.id}",
                "email": email,
                "name": kakao_user.nickname or "카카오 사용자",
                "picture": kakao_user.profile_image_url,
                "verified_email": kakao_user.email_verified if kakao_user.email else False,
                "provider": OAuthProvider.KAKAO,
                "provider_id": str(kakao_user.id)
            }
            user = db.create_user(user_data)
        
        access_token = AuthService.create_access_token(data={"sub": user.email})
        db.add_session(access_token, user.email)
        
        return UserResponse(user=user, access_token=access_token)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"카카오 OAuth 인증 실패: {str(e)}"
        )

# 공통 엔드포인트들
@router.get("/me", response_model=User)
async def get_current_user_profile(current_user: User = Depends(AuthService.get_current_user)):
    """현재 사용자 프로필 조회"""
    return current_user

@router.put("/me", response_model=User)
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

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """로그아웃"""
    token = credentials.credentials
    db.remove_session(token)
    return {"message": "성공적으로 로그아웃되었습니다."}