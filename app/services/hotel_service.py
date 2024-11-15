from typing import Optional

from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.di.dependencies import get_hotel_repository
from app.models.hotel import Hotel
from app.models.repository.hotel_reposiotry_abs import HotelRepositoryInterface
from app.schemas.request import CreateHotelBody
from app.schemas.response import HotelResponse


class HotelService:
    def __init__(self):
        self.hotel_db: Optional[HotelRepositoryInterface] = None

    async def _get_hotel_db(self) -> HotelRepositoryInterface:
        if self.hotel_db is None:
            self.hotel_db = await get_hotel_repository()
        return self.hotel_db

    async def get_all_hotels(self):
        db = await self._get_hotel_db()
        hotels = await db.get_all_hotels()

        if not hotels:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No hotels found")

        return [HotelResponse(hotel_id=str(hotel.hotel_id), name=hotel.name, address=hotel.address) for hotel in hotels]

    async def create_hotel(self, hotel_body: CreateHotelBody):
        db = await self._get_hotel_db()
        new_hotel = Hotel(hotel_id=None, name=hotel_body.name, address=hotel_body.address)
        hotel_id = await db.upload_hotel(new_hotel)
        return {"hotel_id": str(hotel_id)}
