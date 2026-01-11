from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime
from app.db.models.term_employee import EmploymentStatus


class TermEmployeeBase(BaseModel):
    """기간제 인력 기본 스키마"""
    name: str = Field(..., min_length=1, max_length=255, description="이름")
    birthdate: date = Field(..., description="생년월일")
    address: Optional[str] = Field(None, max_length=500, description="주소")
    department_id: int = Field(..., description="부서 ID")
    employment_start_date: date = Field(..., description="재직기간 시작")
    employment_end_date: date = Field(..., description="재직기간 종료")
    position: Optional[str] = Field(None, max_length=255, description="직종")
    manager_name: Optional[str] = Field(None, max_length=255, description="담당자 이름")
    manager_number: Optional[str] = Field(None, max_length=20, description="담당자 연락처")
    notes: Optional[str] = Field(None, max_length=1000, description="비고")


class TermEmployeeCreate(TermEmployeeBase):
    """기간제 인력 생성 스키마"""
    status: EmploymentStatus = Field(default=EmploymentStatus.ACTIVE, description="고용 상태")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "홍길동",
                "birthdate": "1990-01-01",
                "address": "서울시 강남구",
                "department_id": 1,
                "employment_start_date": "2024-01-01",
                "employment_end_date": "2024-12-31",
                "status": "active",
                "position": "행정직",
                "manager_name": "김담당",
                "manager_number": "010-1234-5678",
                "notes": ""
            }
        }


class TermEmployeeUpdate(BaseModel):
    """기간제 인력 수정 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="이름")
    birthdate: Optional[date] = Field(None, description="생년월일")
    address: Optional[str] = Field(None, max_length=500, description="주소")
    department_id: Optional[int] = Field(None, description="부서 ID")
    employment_start_date: Optional[date] = Field(None, description="재직기간 시작")
    employment_end_date: Optional[date] = Field(None, description="재직기간 종료")
    status: Optional[EmploymentStatus] = Field(None, description="고용 상태")
    position: Optional[str] = Field(None, max_length=255, description="직종")
    manager_name: Optional[str] = Field(None, max_length=255, description="담당자 이름")
    manager_number: Optional[str] = Field(None, max_length=20, description="담당자 연락처")
    notes: Optional[str] = Field(None, max_length=1000, description="비고")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "terminated",
                "notes": "계약 종료"
            }
        }


class TermEmployeeSearch(BaseModel):
    """기간제 인력 검색 스키마"""
    name: str = Field(..., min_length=1, description="이름 (필수)")
    birthdate: Optional[date] = Field(None, description="생년월일 (선택)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "홍길동",
                "birthdate": "1990-01-01"
            }
        }


class TermEmployeeListItem(BaseModel):
    """기간제 인력 목록 아이템 스키마"""
    term_employee_id: int
    name: str
    birthdate: date
    manager_name: Optional[str]
    employment_start_date: date
    employment_end_date: date
    position: Optional[str]
    status: EmploymentStatus

    class Config:
        from_attributes = True


class TermEmployeeResponse(BaseModel):
    """기간제 인력 상세 응답 스키마"""
    term_employee_id: int
    name: str
    birthdate: date
    address: Optional[str]
    department_id: int
    employment_start_date: date
    employment_end_date: date
    status: EmploymentStatus
    position: Optional[str]
    manager_name: Optional[str]
    manager_number: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
