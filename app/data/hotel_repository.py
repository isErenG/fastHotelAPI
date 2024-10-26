import uuid

from typing_extensions import override

from app.models.hotel import Hotel
from app.models.repository.hotel_reposiotry_abs import HotelRepositoryInterface


class HotelRepository(HotelRepositoryInterface):
    def __init__(self):
        super().__init__()

    @override
    async def retrieve_hotel(self, hotel_id: uuid.UUID):
        pass

    @override
    async def upload_hotel(self, hotel: Hotel):
        pass
