from fastapi import APIRouter

from app.data.hotel_repository import HotelRepository
from app.data.user_repository import UserRepository

router = APIRouter()

user_repository = UserRepository()
hotel_repository = HotelRepository()

