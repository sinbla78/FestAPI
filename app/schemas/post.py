from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Post(BaseModel):
    """게시글 모델"""
    id: str = Field(..., description="게시글 ID", example="post_123")
    title: str = Field(..., description="게시글 제목", example="첫 번째 게시글")
    content: str = Field(..., description="게시글 내용", example="안녕하세요, 이것은 게시글 내용입니다.")
    author_email: str = Field(..., description="작성자 이메일", example="user@example.com")
    created_at: str = Field(..., description="생성 일시")
    updated_at: str = Field(..., description="수정 일시")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "post_123",
                "title": "첫 번째 게시글",
                "content": "안녕하세요, 이것은 게시글 내용입니다.",
                "author_email": "user@example.com",
                "created_at": "2024-01-07T12:00:00Z",
                "updated_at": "2024-01-07T12:00:00Z"
            }
        }


class PostCreate(BaseModel):
    """게시글 생성 요청"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="게시글 제목",
        examples=["새 게시글"]
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="게시글 내용",
        examples=["게시글 내용입니다."]
    )

    @field_validator("title", "content")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """공백만 있는 문자열 방지"""
        if not v or not v.strip():
            raise ValueError("공백만 입력할 수 없습니다.")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "title": "새 게시글",
                "content": "게시글 내용입니다."
            }
        }


class PostUpdate(BaseModel):
    """게시글 수정 요청"""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="게시글 제목",
        examples=["수정된 제목"]
    )
    content: Optional[str] = Field(
        None,
        min_length=1,
        max_length=10000,
        description="게시글 내용",
        examples=["수정된 내용"]
    )

    @field_validator("title", "content")
    @classmethod
    def validate_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """공백만 있는 문자열 방지"""
        if v is not None:
            if not v.strip():
                raise ValueError("공백만 입력할 수 없습니다.")
            return v.strip()
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "수정된 제목",
                "content": "수정된 내용"
            }
        }
