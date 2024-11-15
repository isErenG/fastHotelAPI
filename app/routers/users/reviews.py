import uuid

from fastapi import Depends, Path
from fastapi.responses import JSONResponse

from app.models.user import User
from app.routers.users import router
from app.schemas.request import ReviewBody
from app.services.review_service import ReviewService
from app.utils.jwt_helper import get_current_user


@router.get("/reviews")
async def get_all_reviews(service: ReviewService = Depends(ReviewService),
                          current_user: User = Depends(get_current_user)):
    reviews = await service.get_all_reviews()
    return JSONResponse(content=reviews)


@router.post("/reviews")
async def create_review(
        review: ReviewBody,
        service: ReviewService = Depends(ReviewService),
        current_user: User = Depends(get_current_user),
):
    return await service.create_review(review, current_user.user_id)


@router.delete("/reviews/{review_id}")
async def delete_review(
        review_id: uuid.UUID = Path(..., description="The ID of the review to delete"),
        service: ReviewService = Depends(ReviewService),
        current_user: User = Depends(get_current_user),
):
    return await service.delete_review(review_id, current_user.user_id)
