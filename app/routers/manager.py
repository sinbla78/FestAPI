from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.manager import Manager
from app.schemas.manager import (
    ManagerCreate,
    ManagerLogin,
    ManagerResponse,
    ManagerTokenResponse
)
from app.services.manager_service import ManagerService
from app.services.password_service import PasswordService

router = APIRouter(prefix="/manager", tags=["관리자"])


@router.post(
    "/signup",
    response_model=ManagerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="관리자 회원가입",
    description="새로운 관리자 계정을 생성합니다."
)
async def manager_signup(
    manager_data: ManagerCreate,
    db: AsyncSession = Depends(get_db)
):
    """관리자 회원가입"""
    # 중복 username 확인
    result = await db.execute(
        select(Manager).where(Manager.username == manager_data.username)
    )
    existing_manager = result.scalar_one_or_none()

    if existing_manager:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 아이디입니다."
        )

    # 비밀번호 해싱
    hashed_password = PasswordService.hash_password(manager_data.password)

    # 관리자 생성
    new_manager = Manager(
        username=manager_data.username,
        password_hash=hashed_password,
        email=manager_data.email
    )

    db.add(new_manager)
    await db.commit()
    await db.refresh(new_manager)

    return new_manager


@router.post(
    "/login",
    response_model=ManagerTokenResponse,
    summary="관리자 로그인",
    description="관리자 아이디와 비밀번호로 로그인합니다."
)
async def manager_login(
    login_data: ManagerLogin,
    db: AsyncSession = Depends(get_db)
):
    """관리자 로그인"""
    # 관리자 조회
    result = await db.execute(
        select(Manager).where(Manager.username == login_data.username)
    )
    manager = result.scalar_one_or_none()

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다."
        )

    # 비밀번호 검증
    if not PasswordService.verify_password(login_data.password, manager.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다."
        )

    # 토큰 생성
    tokens = ManagerService.create_tokens(manager.username)

    return ManagerTokenResponse(
        manager=manager,
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"]
    )


@router.get(
    "/me",
    response_model=ManagerResponse,
    summary="현재 로그인한 관리자 정보 조회",
    description="인증된 관리자의 정보를 조회합니다."
)
async def get_current_manager(
    username: str = Depends(ManagerService.verify_token),
    db: AsyncSession = Depends(get_db)
):
    """현재 로그인한 관리자 정보 조회"""
    result = await db.execute(
        select(Manager).where(Manager.username == username)
    )
    manager = result.scalar_one_or_none()

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="관리자를 찾을 수 없습니다."
        )

    return manager
