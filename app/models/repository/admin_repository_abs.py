import uuid
from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from app.models.admin import Admin


class AdminRepositoryInterface(ABC):

    @abstractmethod
    async def create_admin(self, name: str, email: str, password: str, start_date: date, end_date: date) -> Admin:
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

    @abstractmethod
    async def get_admin_by_email(self, email: str) -> Optional[Admin]:
        pass
