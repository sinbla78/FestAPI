from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Department(Base):
    """부서 모델"""

    __tablename__ = "departments"

    department_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    department_name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Department(id={self.department_id}, name='{self.department_name}')>"
