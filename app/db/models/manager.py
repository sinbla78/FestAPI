from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Manager(Base):
    """관리자 모델"""

    __tablename__ = "managers"

    manager_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Manager(id={self.manager_id}, username='{self.username}')>"
