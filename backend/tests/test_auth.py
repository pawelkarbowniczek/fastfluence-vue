import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

def test_register_user(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "newpass123",
            "role": "advertiser",
            "display_name": "New User",
            "contact_email": "newuser@example.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "advertiser"
    assert data["display_name"] == "New User"

def test_register_duplicate_email(client: TestClient, test_user):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "newpass123",
            "role": "creator",
            "display_name": "Duplicate User",
            "contact_email": test_user.email
        }
    )
    assert response.status_code == 400

def test_login_user(client: TestClient, test_user):
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": test_user.email,
            "password": "testpass"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient, test_user):
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": test_user.email,
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401