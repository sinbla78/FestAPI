from typing import Dict, Optional, TYPE_CHECKING, List
from datetime import datetime, timedelta
import uuid

if TYPE_CHECKING:
    from app.models import User, Post

#인메모리 DB
class InMemoryDB:
    def __init__(self):
        self.users: Dict[str, "User"] = {}
        self.active_sessions: Dict[str, str] = {}  # token -> user_email
        self.token_blacklist: Dict[str, datetime] = {}  # token -> blacklist_time
        self.posts: Dict[str, "Post"] = {}  # post_id -> Post

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

    # 게시글 CRUD
    def create_post(self, post_data: dict) -> "Post":
        """게시글 생성"""
        from app.models import Post
        post_id = f"post_{uuid.uuid4().hex[:12]}"
        now = datetime.utcnow().isoformat() + "Z"
        post = Post(
            id=post_id,
            created_at=now,
            updated_at=now,
            **post_data
        )
        self.posts[post_id] = post
        return post

    def get_post(self, post_id: str) -> Optional["Post"]:
        """게시글 조회"""
        return self.posts.get(post_id)

    def get_all_posts(self, skip: int = 0, limit: int = 100) -> List["Post"]:
        """모든 게시글 조회 (최신순)"""
        all_posts = list(self.posts.values())
        # 최신순 정렬
        all_posts.sort(key=lambda x: x.created_at, reverse=True)
        return all_posts[skip:skip + limit]

    def get_posts_by_author(self, author_email: str, skip: int = 0, limit: int = 100) -> List["Post"]:
        """특정 작성자의 게시글 조회"""
        author_posts = [post for post in self.posts.values() if post.author_email == author_email]
        author_posts.sort(key=lambda x: x.created_at, reverse=True)
        return author_posts[skip:skip + limit]

    def update_post(self, post_id: str, update_data: dict) -> Optional["Post"]:
        """게시글 수정"""
        post = self.posts.get(post_id)
        if post:
            for key, value in update_data.items():
                if hasattr(post, key) and value is not None:
                    setattr(post, key, value)
            post.updated_at = datetime.utcnow().isoformat() + "Z"
            self.posts[post_id] = post
        return post

    def delete_post(self, post_id: str) -> bool:
        """게시글 삭제"""
        if post_id in self.posts:
            del self.posts[post_id]
            return True
        return False

# 글로벌 데이터베이스 인스턴스
db = InMemoryDB()