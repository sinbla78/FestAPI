import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import db
from app.services import AuthService

client = TestClient(app)


@pytest.fixture
def test_user():
    """테스트용 사용자 생성"""
    user_data = {
        "id": "test_user_123",
        "email": "test@example.com",
        "name": "Test User",
        "picture": None,
        "verified_email": True,
        "provider": "google",
        "provider_id": "123456"
    }
    user = db.create_user(user_data)
    return user


@pytest.fixture
def auth_headers(test_user):
    """인증 헤더 생성"""
    tokens = AuthService.create_tokens(test_user.email)
    db.add_session(tokens["access_token"], test_user.email)
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def test_get_posts_empty():
    """빈 게시글 목록 조회"""
    response = client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_post_without_auth():
    """인증 없이 게시글 작성 시도"""
    post_data = {
        "title": "Test Post",
        "content": "This is a test post"
    }
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 403


def test_create_post_with_auth(auth_headers):
    """인증된 사용자의 게시글 작성"""
    post_data = {
        "title": "Test Post",
        "content": "This is a test post"
    }
    response = client.post("/posts/", json=post_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]
    assert "id" in data
    assert "created_at" in data


def test_get_post_by_id(auth_headers):
    """게시글 상세 조회"""
    # 먼저 게시글 생성
    post_data = {
        "title": "Test Post",
        "content": "This is a test post"
    }
    create_response = client.post("/posts/", json=post_data, headers=auth_headers)
    post_id = create_response.json()["id"]

    # 게시글 조회
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["title"] == post_data["title"]


def test_get_my_posts(auth_headers):
    """내가 작성한 게시글 조회"""
    response = client.get("/posts/me", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_post(auth_headers):
    """게시글 수정"""
    # 게시글 생성
    post_data = {
        "title": "Original Title",
        "content": "Original Content"
    }
    create_response = client.post("/posts/", json=post_data, headers=auth_headers)
    post_id = create_response.json()["id"]

    # 게시글 수정
    update_data = {
        "title": "Updated Title"
    }
    response = client.put(f"/posts/{post_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Original Content"


def test_delete_post(auth_headers):
    """게시글 삭제"""
    # 게시글 생성
    post_data = {
        "title": "Post to Delete",
        "content": "This will be deleted"
    }
    create_response = client.post("/posts/", json=post_data, headers=auth_headers)
    post_id = create_response.json()["id"]

    # 게시글 삭제
    response = client.delete(f"/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 204

    # 삭제 확인
    get_response = client.get(f"/posts/{post_id}")
    assert get_response.status_code == 404


def test_update_other_user_post(auth_headers, test_user):
    """다른 사용자의 게시글 수정 시도"""
    # 다른 사용자의 게시글 생성
    other_user_data = {
        "id": "other_user_456",
        "email": "other@example.com",
        "name": "Other User",
        "picture": None,
        "verified_email": True,
        "provider": "google",
        "provider_id": "456789"
    }
    other_user = db.create_user(other_user_data)
    other_post = db.create_post({
        "title": "Other User's Post",
        "content": "Content",
        "author_email": other_user.email
    })

    # 다른 사용자의 게시글 수정 시도
    update_data = {"title": "Hacked!"}
    response = client.put(f"/posts/{other_post.id}", json=update_data, headers=auth_headers)
    assert response.status_code == 403
