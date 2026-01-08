from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.services import AuthService
from app.models import User
from app.core.database import db

router = APIRouter(prefix="/users", tags=["사용자"])

@router.get(
    "/",
    response_model=List[User],
    summary="모든 사용자 조회",
    description="시스템에 등록된 모든 사용자 목록을 조회합니다. **인증 필요**",
    responses={
        200: {
            "description": "사용자 목록 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "email": "user1@example.com",
                            "name": "김철수",
                            "picture": "https://example.com/avatar1.jpg",
                            "verified_email": True,
                            "provider": "google",
                            "provider_id": "google_123456",
                            "created_at": "2024-01-08T12:00:00Z",
                            "updated_at": "2024-01-08T12:00:00Z"
                        }
                    ]
                }
            }
        },
        401: {"description": "인증 실패"}
    }
)
async def get_all_users(current_user: User = Depends(AuthService.get_current_user)):
    """모든 사용자 조회"""
    return db.get_all_users()


@router.get(
    "/{user_email}",
    response_model=User,
    summary="특정 사용자 조회",
    description="이메일로 특정 사용자 정보를 조회합니다. **인증 필요**",
    responses={
        200: {
            "description": "사용자 조회 성공",
            "content": {
                "application/json": {
                    "example": {
                        "email": "user@example.com",
                        "name": "김철수",
                        "picture": "https://example.com/avatar.jpg",
                        "verified_email": True,
                        "provider": "google",
                        "provider_id": "google_123456",
                        "created_at": "2024-01-08T12:00:00Z",
                        "updated_at": "2024-01-08T12:00:00Z"
                    }
                }
            }
        },
        401: {"description": "인증 실패"},
        404: {
            "description": "사용자를 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "NOT_FOUND",
                            "message": "사용자를 찾을 수 없습니다.",
                            "path": "/users/user@example.com"
                        }
                    }
                }
            }
        }
    }
)
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