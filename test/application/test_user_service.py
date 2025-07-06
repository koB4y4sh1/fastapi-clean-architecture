import pytest
from src.application.user_service import UserService
from src.domain.models.user import User

class DummyRepo:
    def __init__(self):
        self.users = []
    def get_all(self):
        return self.users
    def create(self, user):
        self.users.append(user)
        return user

def test_get_all_users():
    repo = DummyRepo()
    repo.users = [User(id=1, name="A", email="a@example.com")]
    service = UserService(repo)
    result = service.get_all_users()
    assert result == repo.users

def test_create_user():
    repo = DummyRepo()
    service = UserService(repo)
    user = User(id=None, name="B", email="b@example.com")
    created = service.create_user(user)
    assert created in repo.users
    assert created.name == "B" 