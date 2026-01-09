from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    보안 헤더 미들웨어

    OWASP 권장 보안 헤더를 모든 응답에 추가합니다.
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # X-Content-Type-Options: MIME 타입 스니핑 방지
        response.headers["X-Content-Type-Options"] = "nosniff"

        # X-Frame-Options: 클릭재킹 방지
        response.headers["X-Frame-Options"] = "DENY"

        # X-XSS-Protection: XSS 공격 방지 (구형 브라우저용)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Strict-Transport-Security: HTTPS 강제 (프로덕션)
        # 주의: HTTPS가 구성된 후에만 활성화해야 함
        # response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Content-Security-Policy: XSS 및 데이터 인젝션 공격 방지
        # 기본적인 정책 - 필요에 따라 조정
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp_policy

        # Referrer-Policy: Referer 헤더 제어
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions-Policy: 브라우저 기능 접근 제어
        permissions_policy = (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(), "
            "usb=(), "
            "magnetometer=(), "
            "gyroscope=(), "
            "accelerometer=()"
        )
        response.headers["Permissions-Policy"] = permissions_policy

        # X-Permitted-Cross-Domain-Policies: Adobe 제품의 크로스 도메인 요청 제어
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        # Cache-Control: 민감한 데이터 캐싱 방지 (API 응답)
        if request.url.path.startswith("/auth") or "/me" in request.url.path:
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

        return response
