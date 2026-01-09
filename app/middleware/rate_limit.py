from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Dict, Tuple
from collections import defaultdict
import asyncio


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate Limiting 미들웨어

    IP 주소 기반으로 요청 횟수를 제한합니다.
    """

    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour

        # {ip: [(timestamp, count)]}
        self.request_counts: Dict[str, list] = defaultdict(list)
        self._cleanup_task = None

    async def dispatch(self, request: Request, call_next):
        # Health check 엔드포인트는 rate limit 제외
        if request.url.path.startswith("/health"):
            return await call_next(request)

        client_ip = self._get_client_ip(request)

        # Rate limit 체크
        is_allowed, retry_after = self._check_rate_limit(client_ip)

        if not is_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "요청 횟수 제한을 초과했습니다. 잠시 후 다시 시도해주세요.",
                        "retry_after": retry_after
                    }
                },
                headers={"Retry-After": str(retry_after)}
            )

        # 요청 처리
        response = await call_next(request)

        # Rate limit 헤더 추가
        remaining = self._get_remaining_requests(client_ip)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response

    def _get_client_ip(self, request: Request) -> str:
        """클라이언트 IP 주소 추출"""
        # X-Forwarded-For 헤더 확인 (프록시 뒤에 있을 경우)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        # X-Real-IP 헤더 확인
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # 직접 연결된 클라이언트 IP
        return request.client.host if request.client else "unknown"

    def _check_rate_limit(self, client_ip: str) -> Tuple[bool, int]:
        """
        Rate limit 체크

        Returns:
            (is_allowed, retry_after_seconds)
        """
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)

        # 오래된 요청 기록 제거
        self.request_counts[client_ip] = [
            ts for ts in self.request_counts[client_ip]
            if ts > hour_ago
        ]

        # 현재 카운트 체크
        minute_requests = sum(1 for ts in self.request_counts[client_ip] if ts > minute_ago)
        hour_requests = len(self.request_counts[client_ip])

        # 분당 제한 체크
        if minute_requests >= self.requests_per_minute:
            oldest_in_minute = min(
                (ts for ts in self.request_counts[client_ip] if ts > minute_ago),
                default=now
            )
            retry_after = int((oldest_in_minute - minute_ago).total_seconds()) + 1
            return False, retry_after

        # 시간당 제한 체크
        if hour_requests >= self.requests_per_hour:
            oldest_in_hour = min(self.request_counts[client_ip], default=now)
            retry_after = int((oldest_in_hour - hour_ago).total_seconds()) + 1
            return False, retry_after

        # 요청 기록 추가
        self.request_counts[client_ip].append(now)
        return True, 0

    def _get_remaining_requests(self, client_ip: str) -> int:
        """남은 요청 횟수 계산"""
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)

        minute_requests = sum(
            1 for ts in self.request_counts[client_ip]
            if ts > minute_ago
        )

        return max(0, self.requests_per_minute - minute_requests)

    async def cleanup_old_records(self):
        """오래된 요청 기록 정리 (백그라운드 태스크)"""
        while True:
            await asyncio.sleep(300)  # 5분마다 실행
            now = datetime.utcnow()
            hour_ago = now - timedelta(hours=1)

            # 1시간 이상 지난 기록 제거
            for ip in list(self.request_counts.keys()):
                self.request_counts[ip] = [
                    ts for ts in self.request_counts[ip]
                    if ts > hour_ago
                ]
                # 빈 기록 제거
                if not self.request_counts[ip]:
                    del self.request_counts[ip]
