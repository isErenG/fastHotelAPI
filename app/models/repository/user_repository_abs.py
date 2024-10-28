import uuid
from abc import ABC, abstractmethod
from typing import List

from app.models.user import User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    async def retrieve_user_with_email(self, user_email: str) -> User:
        pass

    @abstractmethod
    async def retrieve_user_with_id(self, user_id: uuid.UUID) -> User:
        pass

    @abstractmethod
    async def create_user(self, username: str, email: str, password: str) -> Exception:
        pass
