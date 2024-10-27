import uuid
from abc import ABC, abstractmethod
from typing import List

from app.models.user import User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    async def retrieve_user(self, user_id: uuid.UUID) -> User:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> Exception:
        pass
