from fastapi import Depends

from app.data.repository.hotel_repository import HotelRepository
from app.di.dependencies import get_hotel_repository
from app.models.hotel import Hotel
from app.models.user import User
from app.routers.users import router
from app.schemas.request import CreateHotelBody
from app.utils.jwt_helper import get_current_user


@router.get("/hotels")
async def get_hotels(db: HotelRepository = Depends(get_hotel_repository),
                     current_user: User = Depends(get_current_user)):
    return await db.get_all_hotels()


@router.post("/hotels")
async def create_hotel(hotel_body: CreateHotelBody,
                       db: HotelRepository = Depends(get_hotel_repository),
                       current_user: User = Depends(get_current_user)):
    new_hotel = Hotel(hotel_id=None, name=hotel_body.name, address=hotel_body.address)
    hotel_id = await db.upload_hotel(new_hotel)
    return {"hotel_id": hotel_id}
