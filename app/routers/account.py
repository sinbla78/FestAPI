from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.user import User
from app.db.models.department import Department
from app.schemas.user_auth import UserCreate, UserResponse, UserInfoUpdate
from app.services.manager_service import ManagerService
from app.services.password_service import PasswordService
from app.core.messages import ErrorMessages

router = APIRouter(prefix="/accounts", tags=["계정 관리 (관리자 전용)"])


@router.get(
    "/users",
    response_model=List[UserResponse],
    summary="사용자 계정 목록 조회",
    description="관리자가 모든 사용자 계정 목록을 조회합니다."
)
async def get_users(
    username: str = Depends(ManagerService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """사용자 계정 목록 조회 (관리자 전용)"""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="특정 사용자 계정 조회",
    description="관리자가 특정 사용자 계정의 상세 정보를 조회합니다."
)
async def get_user(
    user_id: int,
    username: str = Depends(ManagerService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """특정 사용자 계정 조회 (관리자 전용)"""
    result = await db.execute(
        select(User).where(User.user_id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ErrorMessages.USER_NOT_FOUND"
        )

    return user


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="사용자 계정 생성",
    description="관리자가 새로운 사용자 계정을 생성하고 최초 로그인용 비밀번호를 할당합니다."
)
async def create_user(
    user_data: UserCreate,
    username: str = Depends(ManagerService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """사용자 계정 생성 (관리자 전용)"""
    # 중복 username 확인
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ErrorMessages.USER_ALREADY_EXISTS"
        )

    # 비밀번호 해싱
    hashed_password = PasswordService.hash_password(user_data.password)

    # 사용자 생성 (첫 로그인 상태로)
    new_user = User(
        username=user_data.username,
        password_hash=hashed_password,
        is_first_login=True  # 첫 로그인 상태
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="사용자 계정 수정",
    description="관리자가 사용자 계정의 정보(이름, 연락처, 부서)를 수정합니다."
)
async def update_user(
    user_id: int,
    user_data: UserInfoUpdate,
    username: str = Depends(ManagerService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """사용자 계정 수정 (관리자 전용)"""
    # 사용자 조회
    result = await db.execute(
        select(User).where(User.user_id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ErrorMessages.USER_NOT_FOUND"
        )

    # 부서 변경 시 존재 여부 확인
    if user_data.department_id is not None:
        dept_result = await db.execute(
            select(Department).where(Department.department_id == user_data.department_id)
        )
        department = dept_result.scalar_one_or_none()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ErrorMessages.INVALID_DEPARTMENT"
            )

    # 정보 업데이트
    if user_data.manager_name is not None:
        user.manager_name = user_data.manager_name
    if user_data.manager_number is not None:
        user.manager_number = user_data.manager_number
    if user_data.department_id is not None:
        user.department_id = user_data.department_id

    await db.commit()
    await db.refresh(user)

    return user


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="사용자 계정 삭제",
    description="관리자가 사용자 계정을 삭제합니다."
)
async def delete_user(
    user_id: int,
    username: str = Depends(ManagerService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """사용자 계정 삭제 (관리자 전용)"""
    # 사용자 조회
    result = await db.execute(
        select(User).where(User.user_id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ErrorMessages.USER_NOT_FOUND"
        )

    await db.delete(user)
    await db.commit()

    return None
