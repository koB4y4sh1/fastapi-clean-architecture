from src.interface.user_interface_service import UserInterfaceService
from src.schema.api.user import UserCreateRequest

def test_get_all_users():
    service = UserInterfaceService()
    users = service.get_all_users()
    assert isinstance(users, list)

def test_create_user():
    service = UserInterfaceService()
    req = UserCreateRequest(name="Test", email="test@example.com")
    user = service.create_user(req)
    assert user.name == "Test"
    assert user.email == "test@example.com" 