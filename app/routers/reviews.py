import uuid

from fastapi import HTTPException, Depends
from pydantic import BaseModel

from app.data.repository import review_repository
from app.di.dependencies import get_review_repository
from app.models.user import User
from app.routers import router
from app.utils.jwt_util import get_current_user


@router.get("/reviews")
async def get_users(
        db: review_repository.ReviewRepository = Depends(get_review_repository),
        current_user: User = Depends(get_current_user)
):
    try:
        return await db.get_all_reviews()
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
