from fastapi import APIRouter

from app.di.dependencies import get_user_repository, get_hotel_repository

user_repository = get_user_repository()
hotel_repository = get_hotel_repository()

router = APIRouter()

