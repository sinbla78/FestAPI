from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logging import logger
from typing import Union


class APIException(HTTPException):
    """API 커스텀 예외 기본 클래스"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code or f"ERR_{status_code}"


class BadRequestException(APIException):
    """잘못된 요청 예외"""

    def __init__(self, detail: str = "잘못된 요청입니다.", error_code: str = "BAD_REQUEST"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code,
        )


class UnauthorizedException(APIException):
    """인증 실패 예외"""

    def __init__(self, detail: str = "인증에 실패했습니다.", error_code: str = "UNAUTHORIZED"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code,
        )


class ForbiddenException(APIException):
    """권한 없음 예외"""

    def __init__(self, detail: str = "권한이 없습니다.", error_code: str = "FORBIDDEN"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code,
        )


class NotFoundException(APIException):
    """리소스를 찾을 수 없음 예외"""

    def __init__(self, detail: str = "요청한 리소스를 찾을 수 없습니다.", error_code: str = "NOT_FOUND"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code,
        )


class ConflictException(APIException):
    """리소스 충돌 예외"""

    def __init__(self, detail: str = "리소스 충돌이 발생했습니다.", error_code: str = "CONFLICT"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code,
        )


class InternalServerException(APIException):
    """서버 내부 오류 예외"""

    def __init__(self, detail: str = "서버 내부 오류가 발생했습니다.", error_code: str = "INTERNAL_SERVER_ERROR"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code,
        )


async def api_exception_handler(request: Request, exc: APIException):
    """API 예외 핸들러"""
    logger.error(f"API Exception: {exc.error_code} - {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
                "path": str(request.url.path),
            }
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """입력 검증 실패 예외 핸들러"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    logger.warning(f"Validation Error: {errors} - Path: {request.url.path}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "입력 데이터 검증에 실패했습니다.",
                "details": errors,
                "path": str(request.url.path),
            }
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """일반 예외 핸들러"""
    logger.exception(f"Unexpected error: {str(exc)} - Path: {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "서버 내부 오류가 발생했습니다.",
                "path": str(request.url.path),
            }
        },
    )
