# 멀티스테이지 빌드 - 빌드 스테이지
FROM python:3.11-slim as builder

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치 (빌드에 필요)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사
COPY requirements-prod.txt .

# 가상환경 생성 및 패키지 설치
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-prod.txt


# 최종 런타임 스테이지
FROM python:3.11-slim

# 비root 사용자 생성
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /app/logs && \
    chown -R appuser:appuser /app

# 작업 디렉토리 설정
WORKDIR /app

# 빌더 스테이지에서 가상환경 복사
COPY --from=builder /opt/venv /opt/venv

# 애플리케이션 코드 복사
COPY --chown=appuser:appuser ./app ./app
COPY --chown=appuser:appuser .env.example .env.example

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/opt/venv/bin:$PATH"
ENV ENVIRONMENT=production

# 비root 사용자로 전환
USER appuser

# 포트 노출
EXPOSE 8000

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/liveness')" || exit 1

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
