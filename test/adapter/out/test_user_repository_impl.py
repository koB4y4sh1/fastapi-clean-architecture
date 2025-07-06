from src.adapter.out.user_repository_impl import InMemoryUserRepository
from src.domain.models.user import User

def test_get_all():
    repo = InMemoryUserRepository()
    users = repo.get_all()
    assert isinstance(users, list)
    assert all(isinstance(u, User) for u in users) 