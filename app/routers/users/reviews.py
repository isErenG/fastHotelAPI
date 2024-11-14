import uuid

from fastapi import Depends
from pydantic import BaseModel

from app.data.repository import review_repository
from app.di.dependencies import get_review_repository
from app.models.review import Review
from app.models.user import User
from app.routers.users import router
from app.utils.jwt_helper import get_current_user


@router.get("/reviews")
async def get_users(
        db: review_repository.ReviewRepository = Depends(get_review_repository),
        current_user: User = Depends(get_current_user)
):
    return await db.get_all_reviews()


class ReviewBody(BaseModel):
    hotelID: uuid.UUID
    rating: int
    comments: str


@router.post("/reviews")
async def create_user(
        review: ReviewBody,
        db: review_repository.ReviewRepository = Depends(get_review_repository),
        current_user: User = Depends(get_current_user)):
    review_id = uuid.uuid4()

    new_review = Review(review_id=review_id,
                        rating=review.rating,
                        user_id=current_user.user_id,
                        hotel_id=review.hotelID,
                        comment=review.comments)

    await db.upload_review(new_review)

    return {"review_id": review_id}
