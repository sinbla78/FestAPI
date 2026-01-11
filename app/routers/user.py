from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.user import User
from app.db.models.department import Department
from app.schemas.user_auth import (
    UserLogin,
    FirstLoginInfoUpdate,
    UserInfoUpdate,
    PasswordChange,
    UserResponse,
    UserTokenResponse
)
from app.services.user_service import UserService
from app.services.password_service import PasswordService

router = APIRouter(prefix="/user", tags=["사용자"])


@router.post(
    "/login",
    response_model=UserTokenResponse,
    summary="사용자 로그인",
    description="사용자 아이디와 비밀번호로 로그인합니다."
)
async def user_login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """사용자 로그인"""
    # 사용자 조회
    result = await db.execute(
        select(User).where(User.username == login_data.username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다."
        )

    # 비밀번호 검증
    if not PasswordService.verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다."
        )

    # 토큰 생성
    tokens = UserService.create_tokens(user.username)

    return UserTokenResponse(
        user=user,
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"],
        is_first_login=user.is_first_login
    )


@router.put(
    "/first-login",
    response_model=UserResponse,
    summary="첫 로그인 정보 입력",
    description="첫 로그인 시 담당자 정보와 새 비밀번호를 입력합니다."
)
async def update_first_login_info(
    info: FirstLoginInfoUpdate,
    username: str = Depends(UserService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """첫 로그인 정보 입력"""
    # 사용자 조회
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )

    # 첫 로그인이 아닌 경우
    if not user.is_first_login:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 첫 로그인 정보를 입력했습니다."
        )

    # 부서 존재 여부 확인
    dept_result = await db.execute(
        select(Department).where(Department.department_id == info.department_id)
    )
    department = dept_result.scalar_one_or_none()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 부서입니다."
        )

    # 정보 업데이트
    user.manager_name = info.manager_name
    user.manager_number = info.manager_number
    user.department_id = info.department_id
    user.password_hash = PasswordService.hash_password(info.new_password)
    user.is_first_login = False

    await db.commit()
    await db.refresh(user)

    return user


@router.get(
    "/me",
    response_model=UserResponse,
    summary="현재 로그인한 사용자 정보 조회",
    description="인증된 사용자의 정보를 조회합니다."
)
async def get_current_user(
    username: str = Depends(UserService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """현재 로그인한 사용자 정보 조회"""
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )

    return user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="사용자 정보 수정",
    description="사용자의 개인정보(이름, 연락처, 부서)를 수정합니다."
)
async def update_user_info(
    info: UserInfoUpdate,
    username: str = Depends(UserService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """사용자 정보 수정"""
    # 사용자 조회
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )

    # 부서 변경 시 존재 여부 확인
    if info.department_id is not None:
        dept_result = await db.execute(
            select(Department).where(Department.department_id == info.department_id)
        )
        department = dept_result.scalar_one_or_none()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 부서입니다."
            )

    # 정보 업데이트
    if info.manager_name is not None:
        user.manager_name = info.manager_name
    if info.manager_number is not None:
        user.manager_number = info.manager_number
    if info.department_id is not None:
        user.department_id = info.department_id

    await db.commit()
    await db.refresh(user)

    return user


@router.put(
    "/change-password",
    response_model=dict,
    summary="비밀번호 변경",
    description="현재 비밀번호를 확인하고 새 비밀번호로 변경합니다."
)
async def change_password(
    password_data: PasswordChange,
    username: str = Depends(UserService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """비밀번호 변경"""
    # 사용자 조회
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )

    # 현재 비밀번호 확인
    if not PasswordService.verify_password(password_data.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="현재 비밀번호가 올바르지 않습니다."
        )

    # 새 비밀번호로 변경
    user.password_hash = PasswordService.hash_password(password_data.new_password)

    await db.commit()

    return {"message": "비밀번호가 성공적으로 변경되었습니다."}
