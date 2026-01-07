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
