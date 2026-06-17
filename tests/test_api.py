# tests/test_api.py
import secrets
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test server health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_user_registration_success():
    """Test successful user registration with unique username"""
    # Generate unique username to avoid conflicts
    unique_id = secrets.token_hex(4)
    user_data = {
        "name": f"testuser_{unique_id}",
        "password": "securepassword123",
        "email": f"test_{unique_id}@example.com",
        "experience_years": 2,
        "target_market": "GLOBAL",
        "skills": ["Python", "Docker"],
        "favorite_source_ids": []
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert "ACT-" in data["telegram_activation_code"]

def test_user_registration_duplicate():
    """Test prevention of duplicate username registration"""
    unique_id = secrets.token_hex(4)
    user_data = {
        "name": f"duplicate_{unique_id}",
        "password": "securepassword123",
        "email": f"dup_{unique_id}@example.com",
        "experience_years": 2,
        "target_market": "GLOBAL",
        "skills": ["Python"],
        "favorite_source_ids": []
    }
    # First registration
    response1 = client.post("/users/", json=user_data)
    assert response1.status_code == 201
    
    # Second registration with same username
    response2 = client.post("/users/", json=user_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]