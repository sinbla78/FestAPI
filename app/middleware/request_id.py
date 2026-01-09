from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
from contextvars import ContextVar
from app.core.logging import logger

# Context variable for request ID
request_id_context: ContextVar[str] = ContextVar("request_id", default="")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Request ID 트래킹 미들웨어

    모든 요청에 고유 ID를 할당하고 응답 헤더에 포함시킵니다.
    로그 추적 및 디버깅에 유용합니다.
    """

    def __init__(self, app, header_name: str = "X-Request-ID"):
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next):
        # 클라이언트가 제공한 Request ID가 있으면 사용, 없으면 생성
        request_id = request.headers.get(self.header_name)

        if not request_id:
            request_id = str(uuid.uuid4())

        # Context에 request ID 저장
        request_id_context.set(request_id)

        # Request state에도 저장 (라우터에서 접근 가능)
        request.state.request_id = request_id

        # 로그에 request ID 포함
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"- Client: {request.client.host if request.client else 'unknown'}"
        )

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"[{request_id}] Request failed: {str(e)}")
            raise

        # 응답 헤더에 Request ID 추가
        response.headers[self.header_name] = request_id

        # 로그에 응답 상태 기록
        logger.info(f"[{request_id}] Response status: {response.status_code}")

        return response


def get_request_id() -> str:
    """현재 요청의 Request ID 반환"""
    return request_id_context.get()
