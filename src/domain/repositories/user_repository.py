from abc import ABC, abstractmethod
from typing import List
from src.domain.models.user import User

class UserRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def create(self, user:User) -> User:
        pass