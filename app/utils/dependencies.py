from fastapi import Depends
from app.models import User
from app.services.auth_service import AuthService
from app.core.database import db as database


def get_current_user(current_user: User = Depends(AuthService.get_current_user)) -> User:
    """현재 인증된 사용자 의존성"""
    return current_user


def get_db():
    """데이터베이스 인스턴스 의존성"""
    return database
