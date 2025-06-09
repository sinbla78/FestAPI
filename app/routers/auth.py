from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse

from app.auth import AuthService, security
from app.models import User, UserResponse, UserUpdate
from app.database import db

router = APIRouter(prefix="/auth", tags=["인증"])

@router.get("/google")
async def google_login():
    """Google OAuth 로그인 시작"""
    google_auth_url = AuthService.get_google_auth_url()
    return RedirectResponse(url=google_auth_url)

@router.get("/google/callback")
async def google_callback(code: str) -> UserResponse:
    """Google OAuth 콜백 처리"""
    # Google에서 사용자 정보 가져오기
    google_user = await AuthService.get_google_user_info(code)
    
    # 기존 사용자 확인 또는 새 사용자 생성
    user = db.get_user_by_email(google_user.email)
    if not user:
        user_data = {
            "id": google_user.id,
            "email": google_user.email,
            "name": google_user.name,
            "picture": google_user.picture,
            "verified_email": google_user.verified_email
        }
        user = db.create_user(user_data)
    
    # JWT 토큰 생성
    access_token = AuthService.create_access_token(data={"sub": user.email})
    db.add_session(access_token, user.email)
    
    return UserResponse(
        user=user,
        access_token=access_token
    )

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