import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user_success():
    token = "Bearer testtoken"
    data = {"name": "テストユーザー", "email": "test@example.com"}
    response = client.post("/api/users", json=data, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]

def test_create_user_unauthorized():
    data = {"name": "テストユーザー", "email": "test@example.com"}
    response = client.post("/api/users", json=data)
    assert response.status_code == 401 