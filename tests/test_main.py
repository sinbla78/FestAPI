import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """루트 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["status"] == "running"


def test_health_check():
    """헬스 체크 엔드포인트 테스트"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_test_endpoint():
    """테스트 엔드포인트 테스트"""
    response = client.get("/test")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_docs_available():
    """API 문서 접근 가능 여부 테스트"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    """OpenAPI 스키마 접근 가능 여부 테스트"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "info" in data
    assert "paths" in data


def test_health_liveness():
    """Liveness 프로브 테스트"""
    response = client.get("/health/liveness")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


def test_health_readiness():
    """Readiness 프로브 테스트"""
    response = client.get("/health/readiness")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "checks" in data


def test_metrics_endpoint():
    """메트릭 엔드포인트 테스트"""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data
    assert "service" in data
    assert "system" in data
    assert "database" in data
    assert data["service"]["name"] == "FestAPI"


def test_api_version_info():
    """API 버전 정보 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "api" in data
    assert "current_version" in data["api"]
    assert "supported_versions" in data["api"]


def test_security_headers():
    """보안 헤더 존재 확인"""
    response = client.get("/")
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "X-XSS-Protection" in response.headers
    assert "Content-Security-Policy" in response.headers


def test_request_id_header():
    """Request ID 헤더 테스트"""
    response = client.get("/")
    assert "X-Request-ID" in response.headers
    request_id = response.headers["X-Request-ID"]
    assert len(request_id) > 0


def test_rate_limit_headers():
    """Rate Limit 헤더 테스트"""
    response = client.get("/")
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
