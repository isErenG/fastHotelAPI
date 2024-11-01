import uuid
from typing import Annotated
from fastapi import Body, HTTPException, Depends
from pydantic import BaseModel, Field
from starlette import status

from app.data.repository import user_repository
from app.routers import router
from app.routers.schemas.schemas import TokenData
from app.di.dependencies import get_user_repository
from app.utils.jwt_util import verify_authentication


@router.get("/reviews")
async def get_users(
        db: user_repository.UserRepository = Depends(get_user_repository),
        current_user: TokenData = Depends(verify_authentication)
):
    try:
        return await db.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ReviewBody(BaseModel):
    hotelID: uuid.UUID
    rating: int
    comments: str


@router.post("/reviews")
async def create_user(review: ReviewBody):
    try:
        return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
