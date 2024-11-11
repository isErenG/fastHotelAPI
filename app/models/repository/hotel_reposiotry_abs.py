import uuid
from abc import ABC, abstractmethod
from typing import List

from app.models.hotel import Hotel


class HotelRepositoryInterface(ABC):

    @abstractmethod
    async def get_all_hotels(self) -> List[Hotel]:
        pass

    @abstractmethod
    async def retrieve_hotel(self, hotel_id: uuid.UUID):
        pass

    @abstractmethod
    async def upload_hotel(self, hotel: Hotel) -> uuid.UUID:
        pass
