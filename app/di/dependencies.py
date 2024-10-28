# app/dependencies.py
from app.data.repository.user_repository import UserRepository
from app.models.repository.hotel_reposiotry_abs import HotelRepositoryInterface
from app.data.repository.hotel_repository import HotelRepository
from app.models.repository.user_repository_abs import UserRepositoryInterface


def get_hotel_repository() -> HotelRepositoryInterface:
    return HotelRepository()


def get_user_repository() -> UserRepositoryInterface:
    return UserRepository()
