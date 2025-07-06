from typing import List
from src.domain.repositories.user_repository import UserRepository
from src.domain.models.user import User

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_all_users(self, id) -> List[User]:
        return self.repo.get_all()

    def create_user(self, user: User) -> User:
            # DBから最新IDを取得
            latest_id = 1
            user.id = latest_id
            return self.repo.create(user)