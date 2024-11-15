from fastapi import Depends

from app.models.user import User
from app.routers.users import router
from app.schemas.request import CreateHotelBody
from app.services.hotel_service import HotelService
from app.utils.jwt_helper import get_current_user


@router.get("/hotels")
async def get_hotels(service: HotelService = Depends(HotelService),
                     current_user: User = Depends(get_current_user)):
    return await service.get_all_hotels()


@router.post("/hotels")
async def create_hotel(hotel_body: CreateHotelBody,
                       service: HotelService = Depends(HotelService),
                       current_user: User = Depends(get_current_user)):
    return await service.create_hotel(hotel_body)
