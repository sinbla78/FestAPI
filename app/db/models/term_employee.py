from sqlalchemy import Column, BigInteger, String, Date, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class EmploymentStatus(str, enum.Enum):
    """고용 상태"""
    ACTIVE = "active"  # 재직중
    TERMINATED = "terminated"  # 퇴사
    ON_LEAVE = "on_leave"  # 휴직


class TermEmployee(Base):
    """기간제 인력 모델"""

    __tablename__ = "term_employees"

    term_employee_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)  # 이름
    birthdate = Column(Date, nullable=False, index=True)  # 생년월일
    address = Column(String(500), nullable=True)  # 주소
    department_id = Column(BigInteger, ForeignKey("departments.department_id", ondelete="CASCADE"), nullable=False, index=True)
    employment_start_date = Column(Date, nullable=False)  # 재직기간 시작
    employment_end_date = Column(Date, nullable=False)  # 재직기간 종료
    status = Column(SQLEnum(EmploymentStatus), nullable=False, default=EmploymentStatus.ACTIVE, index=True)
    position = Column(String(255), nullable=True)  # 직종
    manager_name = Column(String(255), nullable=True)  # 담당자 이름
    manager_number = Column(String(20), nullable=True)  # 담당자 연락처
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 관계 설정
    department = relationship("Department", backref="term_employees")

    def __repr__(self):
        return f"<TermEmployee(id={self.term_employee_id}, name='{self.name}', department_id={self.department_id}, status='{self.status}')>"
