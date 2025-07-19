from src.application.user_service import UserService
from src.schema.api.user import UserCreateRequest, UserResponse
from src.domain.models.user import User

class UserInterfaceService:
    def __init__(self, service: UserService):
        self.service = service

    def get_all_users(self, id: int|None) -> list[UserResponse]:
        return self.service.get_all_users(id)

    def create_user(self, user_data: UserCreateRequest) -> UserResponse:
        user = User(
            id=None,
            name=user_data.name,
            email=user_data.email

        )
        return self.service.create_user(user)