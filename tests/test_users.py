from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from tests.conftest import get_test_db

app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/users/register",
        json={
            "email": "pytest@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "pytest@example.com"

def test_register_duplicate_user():
    client.post(
        "/users/register",
        json={
            "email": "duplicate@example.com",
            "password": "TestPassword123"
        }
    )
    response = client.post(
        "/users/register",
        json={
            "email": "duplicate@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 409

def test_login_user():
    client.post(
        "/users/register",
        json={
            "email": "login@example.com",
            "password": "TestPassword123"
        }
    )

    response = client.post(
        "/users/login",
        data={
            "username": "login@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    client.post(
        "/users/register",
        json={
            "email": "wrongpass@example.com",
            "password": "TestPassword123"
        }
    )

    response = client.post(
        "/users/login",
        data={
            "username": "wrongpass@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401

def test_invalid_token():
    response = client.get(
        "/jobs",
        headers={
            "Authorization": "Bearer fake-token"
        }
    )

    assert response.status_code == 401

def test_access_protected_endpoint():
    client.post(
        "/users/register",
        json={
            "email": "protected@example.com",
            "password": "TestPassword123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "protected@example.com",
            "password": "TestPassword123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

def test_user_cannot_see_other_users_jobs():
    # User A
    client.post(
        "/users/register",
        json={
            "email": "usera@example.com",
            "password": "TestPassword123"
        }
    )

    login_a = client.post(
        "/users/login",
        data={
            "username": "usera@example.com",
            "password": "TestPassword123"
        }
    )

    token_a = login_a.json()["access_token"]

    # Create company
    company_response = client.post(
        "/companies",
        json={
            "name": "Test Company",
            "website": "https://testcompany.com"
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    company_id = company_response.json()["id"]

    # Create job as User A
    client.post(
        f"/companies/{company_id}/jobs",
        json={
            "title": "Backend Developer",
            "description": "Test job",
            "location": "Pune"
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    # User B
    client.post(
        "/users/register",
        json={
            "email": "userb@example.com",
            "password": "TestPassword123"
        }
    )

    login_b = client.post(
        "/users/login",
        data={
            "username": "userb@example.com",
            "password": "TestPassword123"
        }
    )

    token_b = login_b.json()["access_token"]

    # User B requests jobs
    response = client.get(
        "/jobs",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 200
    assert response.json() == []