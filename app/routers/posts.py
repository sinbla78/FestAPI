from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.models import User
from app.schemas import Post, PostCreate, PostUpdate
from app.services import AuthService
from app.core.database import db

router = APIRouter(prefix="/posts", tags=["게시글"])


@router.post(
    "/",
    response_model=Post,
    status_code=status.HTTP_201_CREATED,
    summary="게시글 작성",
    description="""
    새로운 게시글을 작성합니다.

    **인증 필요**: Bearer 토큰을 헤더에 포함해야 합니다.
    """,
    responses={
        201: {"description": "게시글 작성 성공"},
        401: {"description": "인증 실패"}
    }
)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(AuthService.get_current_user)
) -> Post:
    """게시글 작성"""
    post_dict = {
        "title": post_data.title,
        "content": post_data.content,
        "author_email": current_user.email
    }
    post = db.create_post(post_dict)
    return post


@router.get(
    "/",
    response_model=List[Post],
    summary="게시글 목록 조회",
    description="""
    모든 게시글 목록을 최신순으로 조회합니다.

    페이지네이션을 지원합니다.
    """,
    responses={
        200: {"description": "게시글 목록 조회 성공"}
    }
)
async def get_posts(skip: int = 0, limit: int = 100) -> List[Post]:
    """게시글 목록 조회 (최신순)"""
    posts = db.get_all_posts(skip=skip, limit=limit)
    return posts


@router.get(
    "/me",
    response_model=List[Post],
    summary="내가 작성한 게시글 조회",
    description="""
    현재 로그인한 사용자가 작성한 게시글 목록을 조회합니다.

    **인증 필요**: Bearer 토큰을 헤더에 포함해야 합니다.
    """,
    responses={
        200: {"description": "내 게시글 조회 성공"},
        401: {"description": "인증 실패"}
    }
)
async def get_my_posts(
    current_user: User = Depends(AuthService.get_current_user),
    skip: int = 0,
    limit: int = 100
) -> List[Post]:
    """내가 작성한 게시글 조회"""
    posts = db.get_posts_by_author(current_user.email, skip=skip, limit=limit)
    return posts


@router.get(
    "/{post_id}",
    response_model=Post,
    summary="게시글 상세 조회",
    description="""
    특정 게시글의 상세 정보를 조회합니다.
    """,
    responses={
        200: {"description": "게시글 조회 성공"},
        404: {"description": "게시글을 찾을 수 없음"}
    }
)
async def get_post(post_id: str) -> Post:
    """게시글 상세 조회"""
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )
    return post


@router.put(
    "/{post_id}",
    response_model=Post,
    summary="게시글 수정",
    description="""
    게시글을 수정합니다.

    **인증 필요**: Bearer 토큰을 헤더에 포함해야 합니다.

    **권한**: 게시글 작성자만 수정할 수 있습니다.
    """,
    responses={
        200: {"description": "게시글 수정 성공"},
        401: {"description": "인증 실패"},
        403: {"description": "권한 없음 (작성자가 아님)"},
        404: {"description": "게시글을 찾을 수 없음"}
    }
)
async def update_post(
    post_id: str,
    post_update: PostUpdate,
    current_user: User = Depends(AuthService.get_current_user)
) -> Post:
    """게시글 수정"""
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )

    # 작성자 확인
    if post.author_email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="게시글을 수정할 권한이 없습니다."
        )

    update_data = post_update.dict(exclude_unset=True)
    updated_post = db.update_post(post_id, update_data)
    return updated_post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="게시글 삭제",
    description="""
    게시글을 삭제합니다.

    **인증 필요**: Bearer 토큰을 헤더에 포함해야 합니다.

    **권한**: 게시글 작성자만 삭제할 수 있습니다.
    """,
    responses={
        204: {"description": "게시글 삭제 성공"},
        401: {"description": "인증 실패"},
        403: {"description": "권한 없음 (작성자가 아님)"},
        404: {"description": "게시글을 찾을 수 없음"}
    }
)
async def delete_post(
    post_id: str,
    current_user: User = Depends(AuthService.get_current_user)
):
    """게시글 삭제"""
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )

    # 작성자 확인
    if post.author_email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="게시글을 삭제할 권한이 없습니다."
        )

    db.delete_post(post_id)
    return None
