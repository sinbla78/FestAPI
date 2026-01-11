from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.department import Department
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentListItem
)
from app.services.user_service import UserService
from app.services.manager_service import ManagerService

router = APIRouter(prefix="/departments", tags=["부서"])


@router.get(
    "",
    response_model=List[DepartmentListItem],
    summary="부서 목록 조회",
    description="모든 부서 목록을 조회합니다. (사용자/관리자 모두 접근 가능)"
)
async def get_departments(
    db: AsyncSession = Depends(get_db)
):
    """부서 목록 조회"""
    result = await db.execute(select(Department))
    departments = result.scalars().all()
    return departments


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
    summary="부서 상세 조회",
    description="특정 부서의 상세 정보를 조회합니다."
)
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db)
):
    """부서 상세 조회"""
    result = await db.execute(
        select(Department).where(Department.department_id == department_id)
    )
    department = result.scalar_one_or_none()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="부서를 찾을 수 없습니다."
        )

    return department


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="부서 생성 (관리자 전용)",
    description="새로운 부서를 생성합니다."
)
async def create_department(
    department_data: DepartmentCreate,
    username: str = Depends(ManagerService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """부서 생성 (관리자 전용)"""
    # 중복 부서명 확인
    result = await db.execute(
        select(Department).where(Department.department_name == department_data.department_name)
    )
    existing_department = result.scalar_one_or_none()

    if existing_department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 부서명입니다."
        )

    # 부서 생성
    new_department = Department(
        department_name=department_data.department_name,
        description=department_data.description
    )

    db.add(new_department)
    await db.commit()
    await db.refresh(new_department)

    return new_department


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse,
    summary="부서 정보 수정 (관리자 전용)",
    description="부서 정보를 수정합니다."
)
async def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    username: str = Depends(ManagerService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """부서 정보 수정 (관리자 전용)"""
    # 부서 조회
    result = await db.execute(
        select(Department).where(Department.department_id == department_id)
    )
    department = result.scalar_one_or_none()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="부서를 찾을 수 없습니다."
        )

    # 부서명 중복 확인 (변경하는 경우)
    if department_data.department_name is not None:
        dup_result = await db.execute(
            select(Department).where(
                Department.department_name == department_data.department_name,
                Department.department_id != department_id
            )
        )
        existing_department = dup_result.scalar_one_or_none()

        if existing_department:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 부서명입니다."
            )

    # 정보 업데이트
    if department_data.department_name is not None:
        department.department_name = department_data.department_name
    if department_data.description is not None:
        department.description = department_data.description

    await db.commit()
    await db.refresh(department)

    return department


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="부서 삭제 (관리자 전용)",
    description="부서를 삭제합니다."
)
async def delete_department(
    department_id: int,
    username: str = Depends(ManagerService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """부서 삭제 (관리자 전용)"""
    # 부서 조회
    result = await db.execute(
        select(Department).where(Department.department_id == department_id)
    )
    department = result.scalar_one_or_none()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="부서를 찾을 수 없습니다."
        )

    await db.delete(department)
    await db.commit()

    return None
