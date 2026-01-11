from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.session import get_db
from app.db.models.term_employee import TermEmployee
from app.db.models.department import Department
from app.schemas.term_employee import (
    TermEmployeeCreate,
    TermEmployeeUpdate,
    TermEmployeeSearch,
    TermEmployeeListItem,
    TermEmployeeResponse
)
from app.services.user_service import UserService

router = APIRouter(prefix="/term-employees", tags=["기간제 인력"])


@router.get(
    "/search",
    response_model=List[TermEmployeeListItem],
    summary="기간제 인력 검색",
    description="이름(필수)과 생년월일(선택)로 기간제 인력을 검색합니다."
)
async def search_term_employees(
    name: str = Query(..., description="이름 (필수)"),
    birthdate: Optional[str] = Query(None, description="생년월일 (선택, YYYY-MM-DD 형식)"),
    username: str = Depends(UserService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """기간제 인력 검색"""
    # 기본 검색 조건 (이름)
    conditions = [TermEmployee.name.like(f"%{name}%")]

    # 생년월일 조건 추가
    if birthdate:
        from datetime import datetime
        try:
            birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d").date()
            conditions.append(TermEmployee.birthdate == birthdate_obj)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="생년월일 형식이 올바르지 않습니다. (YYYY-MM-DD)"
            )

    # 검색 실행
    result = await db.execute(
        select(TermEmployee).where(and_(*conditions))
    )
    employees = result.scalars().all()

    return employees


@router.get(
    "",
    response_model=List[TermEmployeeListItem],
    summary="기간제 인력 목록 조회",
    description="모든 기간제 인력 목록을 조회합니다."
)
async def get_term_employees(
    username: str = Depends(UserService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """기간제 인력 목록 조회"""
    result = await db.execute(select(TermEmployee))
    employees = result.scalars().all()
    return employees


@router.get(
    "/{employee_id}",
    response_model=TermEmployeeResponse,
    summary="기간제 인력 상세 조회",
    description="특정 기간제 인력의 상세 정보를 조회합니다."
)
async def get_term_employee(
    employee_id: int,
    username: str = Depends(UserService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """기간제 인력 상세 조회"""
    result = await db.execute(
        select(TermEmployee).where(TermEmployee.term_employee_id == employee_id)
    )
    employee = result.scalar_one_or_none()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="기간제 인력을 찾을 수 없습니다."
        )

    return employee


@router.post(
    "",
    response_model=TermEmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="기간제 인력 등록",
    description="새로운 기간제 인력 정보를 등록합니다."
)
async def create_term_employee(
    employee_data: TermEmployeeCreate,
    username: str = Depends(UserService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """기간제 인력 등록"""
    # 부서 존재 여부 확인
    dept_result = await db.execute(
        select(Department).where(Department.department_id == employee_data.department_id)
    )
    department = dept_result.scalar_one_or_none()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 부서입니다."
        )

    # 기간제 인력 생성
    new_employee = TermEmployee(
        name=employee_data.name,
        birthdate=employee_data.birthdate,
        address=employee_data.address,
        department_id=employee_data.department_id,
        employment_start_date=employee_data.employment_start_date,
        employment_end_date=employee_data.employment_end_date,
        status=employee_data.status,
        position=employee_data.position,
        manager_name=employee_data.manager_name,
        manager_number=employee_data.manager_number,
        notes=employee_data.notes
    )

    db.add(new_employee)
    await db.commit()
    await db.refresh(new_employee)

    return new_employee


@router.put(
    "/{employee_id}",
    response_model=TermEmployeeResponse,
    summary="기간제 인력 정보 수정",
    description="기간제 인력의 정보를 수정합니다."
)
async def update_term_employee(
    employee_id: int,
    employee_data: TermEmployeeUpdate,
    username: str = Depends(UserService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """기간제 인력 정보 수정"""
    # 기간제 인력 조회
    result = await db.execute(
        select(TermEmployee).where(TermEmployee.term_employee_id == employee_id)
    )
    employee = result.scalar_one_or_none()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="기간제 인력을 찾을 수 없습니다."
        )

    # 부서 변경 시 존재 여부 확인
    if employee_data.department_id is not None:
        dept_result = await db.execute(
            select(Department).where(Department.department_id == employee_data.department_id)
        )
        department = dept_result.scalar_one_or_none()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 부서입니다."
            )

    # 정보 업데이트
    update_data = employee_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)

    await db.commit()
    await db.refresh(employee)

    return employee


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="기간제 인력 삭제",
    description="기간제 인력 정보를 삭제합니다."
)
async def delete_term_employee(
    employee_id: int,
    username: str = Depends(UserService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """기간제 인력 삭제"""
    # 기간제 인력 조회
    result = await db.execute(
        select(TermEmployee).where(TermEmployee.term_employee_id == employee_id)
    )
    employee = result.scalar_one_or_none()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="기간제 인력을 찾을 수 없습니다."
        )

    await db.delete(employee)
    await db.commit()

    return None
