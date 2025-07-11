import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlmodel import Session

def get_auth_header(client: TestClient, user_email: str, password: str):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": user_email, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_campaign(client: TestClient, test_user):
    headers = get_auth_header(client, test_user.email, "testpass")
    
    campaign_data = {
        "title": "Test Campaign",
        "description": "Test campaign description",
        "category": "Technologia",
        "media_channel": "Instagram",
        "location": "Warszawa",
        "compensation": "Cash",
        "budget_min": 1000,
        "budget_max": 5000,
        "deadline": (datetime.now() + timedelta(days=30)).isoformat()
    }
    
    response = client.post(
        "/api/v1/campaigns/",
        json=campaign_data,
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Campaign"
    assert data["owner_id"] == test_user.id

def test_create_campaign_creator_forbidden(client: TestClient, test_creator):
    headers = get_auth_header(client, test_creator.email, "creatorpass")
    
    campaign_data = {
        "title": "Test Campaign",
        "description": "Test campaign description",
        "category": "Technologia",
        "media_channel": "Instagram",
        "location": "Warszawa",
        "compensation": "Cash",
        "budget_min": 1000,
        "budget_max": 5000,
        "deadline": (datetime.now() + timedelta(days=30)).isoformat()
    }
    
    response = client.post(
        "/api/v1/campaigns/",
        json=campaign_data,
        headers=headers
    )
    
    assert response.status_code == 403

def test_get_campaigns(client: TestClient, test_user):
    headers = get_auth_header(client, test_user.email, "testpass")
    
    response = client.get("/api/v1/campaigns/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_campaign_validation_missing_budget(client: TestClient, test_user):
    headers = get_auth_header(client, test_user.email, "testpass")
    
    campaign_data = {
        "title": "Test Campaign",
        "description": "Test campaign description",
        "category": "Technologia",
        "media_channel": "Instagram",
        "location": "Warszawa",
        "compensation": "Cash",
        "deadline": (datetime.now() + timedelta(days=30)).isoformat()
    }
    
    response = client.post(
        "/api/v1/campaigns/",
        json=campaign_data,
        headers=headers
    )
    
    assert response.status_code == 400