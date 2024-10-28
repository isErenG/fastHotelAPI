import uuid
from typing import Annotated

from fastapi import Body, HTTPException
from pydantic import BaseModel, Field

from app.routers import router, user_repository


@router.get("/reviews")
async def get_users():
    try:
        return await user_repository.get_all_users()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ReviewBody(BaseModel):
    hotelID: uuid.UUID
    rating: int
    comments: str


@router.post("/reviews")
async def create_user(review: ReviewBody):
    try:
        user_repository.create_user()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
