import pytest
from fastapi.testclient import TestClient

def get_auth_header(client: TestClient, user_email: str, password: str):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": user_email, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_current_user(client: TestClient, test_user):
    headers = get_auth_header(client, test_user.email, "testpass")
    
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["id"] == test_user.id

def test_update_current_user(client: TestClient, test_user):
    headers = get_auth_header(client, test_user.email, "testpass")
    
    update_data = {
        "display_name": "Updated Name",
        "phone": "+48123456789"
    }
    
    response = client.put("/api/v1/users/me", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "Updated Name"
    assert data["phone"] == "+48123456789"

def test_get_user_profile(client: TestClient, test_user, test_creator):
    headers = get_auth_header(client, test_user.email, "testpass")
    
    response = client.get(f"/api/v1/users/{test_creator.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_creator.id
    assert data["display_name"] == test_creator.display_name
    # Phone should be hidden in public profile
    assert "phone" not in data

def test_get_nonexistent_user(client: TestClient, test_user):
    headers = get_auth_header(client, test_user.email, "testpass")
    
    response = client.get("/api/v1/users/999", headers=headers)
    assert response.status_code == 404