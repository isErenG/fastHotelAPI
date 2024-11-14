import uuid
from abc import ABC, abstractmethod

from app.models.admin import Admin


class HotelRepositoryInterface(ABC):

    @abstractmethod
    async def create_admin(self) -> Admin:
        pass

    @abstractmethod
    async def get_admin(self, admin_id: uuid.UUID) -> uuid.UUID:
        pass

    @abstractmethod
    async def remove_admin(self, admin_id: uuid.UUID):
        pass

    @abstractmethod
    async def update_admin(self, admin_id: uuid.UUID) -> uuid.UUID:
        pass
