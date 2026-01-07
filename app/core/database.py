from typing import Dict, Optional, TYPE_CHECKING
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from app.models import User

#인메모리 DB
class InMemoryDB:
    def __init__(self):
        self.users: Dict[str, "User"] = {}
        self.active_sessions: Dict[str, str] = {}  # token -> user_email
        self.token_blacklist: Dict[str, datetime] = {}  # token -> blacklist_time

    def create_user(self, user_data: dict) -> "User":
        from app.models import User
        user = User(**user_data)
        self.users[user.email] = user
        return user

    def get_user_by_email(self, email: str) -> Optional["User"]:
        return self.users.get(email)

    def update_user(self, email: str, update_data: dict) -> Optional["User"]:
        user = self.users.get(email)
        if user:
            for key, value in update_data.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            self.users[email] = user
        return user

    def get_all_users(self) -> list["User"]:
        return list(self.users.values())
    
    def add_session(self, token: str, email: str):
        self.active_sessions[token] = email
    
    def remove_session(self, token: str):
        if token in self.active_sessions:
            del self.active_sessions[token]
    
    def get_active_sessions_count(self) -> int:
        return len(self.active_sessions)

    def add_to_blacklist(self, token: str):
        """토큰을 블랙리스트에 추가"""
        self.token_blacklist[token] = datetime.utcnow()

    def is_token_blacklisted(self, token: str) -> bool:
        """토큰이 블랙리스트에 있는지 확인"""
        return token in self.token_blacklist

    def cleanup_expired_blacklist(self, max_age_days: int = 7):
        """만료된 블랙리스트 토큰 정리 (리프레시 토큰 만료 기간인 7일 기준)"""
        cutoff_time = datetime.utcnow() - timedelta(days=max_age_days)
        expired_tokens = [
            token for token, blacklist_time in self.token_blacklist.items()
            if blacklist_time < cutoff_time
        ]
        for token in expired_tokens:
            del self.token_blacklist[token]
        return len(expired_tokens)

# 글로벌 데이터베이스 인스턴스
db = InMemoryDB()