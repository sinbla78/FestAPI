from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DepartmentBase(BaseModel):
    """부서 기본 스키마"""
    department_name: str = Field(..., min_length=1, max_length=255, description="부서명")
    description: Optional[str] = Field(None, description="부서 설명")


class DepartmentCreate(DepartmentBase):
    """부서 생성 스키마"""
    class Config:
        json_schema_extra = {
            "example": {
                "department_name": "인사과",
                "description": "인사 및 급여 관리"
            }
        }


class DepartmentUpdate(BaseModel):
    """부서 수정 스키마"""
    department_name: Optional[str] = Field(None, min_length=1, max_length=255, description="부서명")
    description: Optional[str] = Field(None, description="부서 설명")

    class Config:
        json_schema_extra = {
            "example": {
                "department_name": "인사총무과",
                "description": "인사, 급여 및 총무 관리"
            }
        }


class DepartmentResponse(BaseModel):
    """부서 응답 스키마"""
    department_id: int
    department_name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DepartmentListItem(BaseModel):
    """부서 목록 아이템 스키마 (간단한 정보만)"""
    department_id: int
    department_name: str

    class Config:
        from_attributes = True
