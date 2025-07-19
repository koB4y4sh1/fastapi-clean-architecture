import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_users_success():
    token = "Bearer testtoken"
    response = client.get("/api/users", headers={"Authorization": token})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_users_unauthorized():
    response = client.get("/api/users")
    assert response.status_code == 401 