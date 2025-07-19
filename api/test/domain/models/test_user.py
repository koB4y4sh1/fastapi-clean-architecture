from src.domain.models.user import User

def test_user_init():
    user = User(id=1, name="Test", email="test@example.com")
    assert user.id == 1
    assert user.name == "Test"
    assert user.email == "test@example.com" 