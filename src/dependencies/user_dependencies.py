# src/di/container.py
from src.application.user_service import UserService
from src.adapter.out.user_repository_impl import InMemoryUserRepository
from src.interface.user_interface_service import UserInterfaceService

def get_user_interface_service() -> UserInterfaceService:
    repo = InMemoryUserRepository()
    service = UserService(repo=repo)
    return UserInterfaceService(service=service)