from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.services import AuthService
from app.models import User
from app.database import db

router = APIRouter(prefix="/users", tags=["사용자"])

@router.get("/", response_model=List[User])
async def get_all_users(current_user: User = Depends(AuthService.get_current_user)):
    """모든 사용자 조회"""
    return db.get_all_users()

@router.get("/{user_email}", response_model=User)
async def get_user_by_email(
    user_email: str, 
    current_user: User = Depends(AuthService.get_current_user)
):
    """특정 사용자 조회"""
    user = db.get_user_by_email(user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    return user