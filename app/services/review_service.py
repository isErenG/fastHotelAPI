import logging
import uuid

from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from app.di.dependencies import get_review_repository
from app.models.repository.review_repository_abs import ReviewRepositoryInterface
from app.models.review import Review
from app.schemas.request import ReviewBody


class ReviewService:
    def __init__(self):
        self.review_db: ReviewRepositoryInterface = None
        self.logger = logging.getLogger(__name__)

    async def _get_review_db(self) -> ReviewRepositoryInterface:
        if self.review_db is None:
            self.logger.debug("Initializing review repository")
            self.review_db = await get_review_repository()
        return self.review_db

    async def get_all_reviews(self):
        self.logger.info("Fetching all reviews from the database")
        db = await self._get_review_db()
        reviews = await db.get_all_reviews()

        if not reviews:
            self.logger.warning("No reviews found in the database")
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No reviews found")

        self.logger.debug(f"Retrieved {len(reviews)} reviews from the database")
        return reviews

    async def create_review(self, review_data: ReviewBody, current_user_id: uuid.UUID):
        self.logger.info(f"Creating a new review by user: {current_user_id} for hotel: {review_data.hotelID}")
        db = await self._get_review_db()

        new_review = Review(
            review_id=uuid.uuid4(),
            rating=review_data.rating,
            user_id=current_user_id,
            hotel_id=review_data.hotelID,
            comment=review_data.comments,
        )

        await db.upload_review(new_review)
        self.logger.info(f"Review created successfully with ID: {new_review.review_id}")

        return {"review_id": str(new_review.review_id)}

    async def delete_review(self, review_id: uuid.UUID, current_user_id: uuid.UUID):
        self.logger.info(f"Attempting to delete review with ID: {review_id} by user: {current_user_id}")
        db = await self._get_review_db()
        review = await db.retrieve_review(review_id)

        if not review:
            self.logger.warning(f"Review with ID {review_id} not found")
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Review not found")

        if review.user_id != current_user_id:
            self.logger.warning(f"User {current_user_id} not authorized to delete review {review_id}")
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not allowed to delete this review")

        await db.delete_review(review_id)
        self.logger.info(f"Review with ID {review_id} deleted successfully")

        return {"message": "Review deleted successfully"}
