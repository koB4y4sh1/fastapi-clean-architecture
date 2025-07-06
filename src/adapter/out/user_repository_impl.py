from typing import List
from src.domain.repositories.user_repository import UserRepository
from src.domain.models.user import User

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = [
            User(id=1, name="Taro Yamada", email="taro@example.com"),
            User(id=2, name="Hanako Suzuki", email="hanako@example.com"),
        ]

    def get_all(self) -> List[User]:
        return self.users
    
    
    def create(self, user: User) -> User:
        self.users.append(user)
        return self.users[0]
