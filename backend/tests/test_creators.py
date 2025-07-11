import pytest
from fastapi.testclient import TestClient

def get_auth_header(client: TestClient, user_email: str, password: str):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": user_email, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_creators(client: TestClient, test_user, test_creator):
    headers = get_auth_header(client, test_user.email, "testpass")
    
    response = client.get("/api/v1/creators/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Check that creator is in the results
    creator_found = any(creator["id"] == test_creator.id for creator in data)
    assert creator_found

def test_get_creators_with_search(client: TestClient, test_user, test_creator):
    headers = get_auth_header(client, test_user.email, "testpass")
    
    response = client.get(
        "/api/v1/creators/", 
        params={"search": "Test Creator"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)