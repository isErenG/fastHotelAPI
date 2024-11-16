import logging
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
        self.logger = logging.getLogger(__name__)

    async def _get_hotel_db(self) -> HotelRepositoryInterface:
        if self.hotel_db is None:
            self.logger.debug("Initializing hotel repository")
            self.hotel_db = await get_hotel_repository()
        return self.hotel_db

    async def get_all_hotels(self):
        self.logger.info("Fetching all hotels from the database")
        db = await self._get_hotel_db()
        hotels = await db.get_all_hotels()

        if not hotels:
            self.logger.warning("No hotels found in the database")
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No hotels found")

        self.logger.debug(f"Retrieved {len(hotels)} hotels from the database")
        return [HotelResponse(hotel_id=str(hotel.hotel_id), name=hotel.name, address=hotel.address) for hotel in hotels]

    async def create_hotel(self, hotel_body: CreateHotelBody):
        self.logger.info(f"Creating a new hotel with name: {hotel_body.name}")
        db = await self._get_hotel_db()
        new_hotel = Hotel(hotel_id=None, name=hotel_body.name, address=hotel_body.address)
        hotel_id = await db.upload_hotel(new_hotel)

        self.logger.info(f"Hotel created with ID: {hotel_id}")
        return {"hotel_id": str(hotel_id)}
