import uuid
from typing import List

from typing_extensions import override

from app.data.repository import cursor
from app.models.hotel import Hotel
from app.models.repository.hotel_reposiotry_abs import HotelRepositoryInterface


class HotelRepository(HotelRepositoryInterface):
    def __init__(self):
        super().__init__()

    @override
    async def get_all_hotels(self) -> List[Hotel]:
        hotel_list = []

        cursor.execute("SELECT * FROM hotels")

        results = cursor.fetchall()

        for row in results:
            hotel_list.append(Hotel(hotelID=row[0], name=row[1], address=row[2]))

        return hotel_list

    @override
    async def retrieve_hotel(self, hotel_id: uuid.UUID):
        pass

    @override
    async def upload_hotel(self, hotel: Hotel):
        pass
