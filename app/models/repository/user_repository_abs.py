import uuid
from abc import ABC, abstractmethod

from app.models.user import User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def retrieve_user(self, user_id: uuid.UUID):
        pass

    @abstractmethod
    async def create_user(self, user: User):
        pass
