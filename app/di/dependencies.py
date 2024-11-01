# app/dependencies.py
from app.data.repository.review_repository import ReviewRepository
from app.data.repository.user_repository import UserRepository
from app.models.repository.hotel_reposiotry_abs import HotelRepositoryInterface
from app.data.repository.hotel_repository import HotelRepository
from app.models.repository.review_repository_abs import ReviewRepositoryInterface
from app.models.repository.user_repository_abs import UserRepositoryInterface


async def get_hotel_repository() -> HotelRepositoryInterface:
    return HotelRepository()


async def get_user_repository() -> UserRepositoryInterface:
    return UserRepository()

async def get_review_repository() -> ReviewRepositoryInterface:
    return ReviewRepository()