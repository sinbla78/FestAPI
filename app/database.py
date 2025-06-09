from typing import Dict, Optional
from app.models import User
from datetime import datetime

#인메모리 DB
class InMemoryDB:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.active_sessions: Dict[str, str] = {}  # token -> user_email
    
    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.users[user.email] = user
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.users.get(email)
    
    def update_user(self, email: str, update_data: dict) -> Optional[User]:
        user = self.users.get(email)
        if user:
            for key, value in update_data.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            self.users[email] = user
        return user
    
    def get_all_users(self) -> list[User]:
        return list(self.users.values())
    
    def add_session(self, token: str, email: str):
        self.active_sessions[token] = email
    
    def remove_session(self, token: str):
        if token in self.active_sessions:
            del self.active_sessions[token]
    
    def get_active_sessions_count(self) -> int:
        return len(self.active_sessions)

# 글로벌 데이터베이스 인스턴스
db = InMemoryDB()