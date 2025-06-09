from fastapi import APIRouter, Depends

from app.auth import AuthService
from app.models import User

router = APIRouter(prefix="/protected", tags=["보호된 엔드포인트"])

@router.get("/")
async def protected_route(current_user: User = Depends(AuthService.get_current_user)):
    """보호된 엔드포인트 예제"""
    return {
        "message": f"안녕하세요, {current_user.name}님! 이것은 보호된 엔드포인트입니다.",
        "user_info": {
            "email": current_user.email,
            "name": current_user.name,
            "verified": current_user.verified_email
        }
    }

@router.get("/admin")
async def admin_route(current_user: User = Depends(AuthService.get_current_user)):
    """관리자 전용 엔드포인트 예제"""
    # 실제로는 사용자 권한 확인 로직이 필요
    return {
        "message": "관리자 페이지에 오신 것을 환영합니다!",
        "admin": current_user.email
    }
