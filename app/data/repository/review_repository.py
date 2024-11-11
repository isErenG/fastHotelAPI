import logging
import uuid
from typing import List, Optional

import psycopg2
from fastapi import HTTPException
from typing_extensions import override

from app.data.repository import cursor
from app.models.repository.review_repository_abs import ReviewRepositoryInterface
from app.models.review import Review


class ReviewRepository(ReviewRepositoryInterface):
    def __init__(self):
        super().__init__()

    @override
    async def get_all_reviews(self) -> List[Review]:
        try:
            review_list = []
            cursor.execute("SELECT * FROM reviews")
            results = cursor.fetchall()

            for row in results:
                review_list.append(Review(review_id=row[0],
                                          user_id=row[1],
                                          hotel_id=row[2],
                                          rating=row[3],
                                          comment=row[4]))
            return review_list

        except Exception as e:
            logging.exception(e)
            raise HTTPException(500, str(e))

    @override
    async def get_reviews_for_hotel(self, hotel_id: uuid.UUID) -> List[Review]:
        review_list = []
        cursor.execute("SELECT * FROM reviews WHERE hotel_id = %s", (hotel_id,))
        results = cursor.fetchall()

        for row in results:
            review_list.append(Review(reviewID=row[0], userID=row[1], hotelID=row[2], rating=row[3], comment=row[4]))

        return review_list

    @override
    async def retrieve_review(self, review_id: uuid.UUID) -> Optional[Review]:
        cursor.execute("SELECT * FROM reviews WHERE review_id = %s", (review_id,))
        row = cursor.fetchone()

        if row:
            return Review(reviewID=row[0], userID=row[1], hotelID=row[2], rating=row[3], comment=row[4])

        return None

    @override
    async def upload_review(self, review: Review):

        try:
            cursor.execute(
                "INSERT INTO reviews (review_id, user_id, hotel_id, rating, comment) VALUES (%s, %s, %s, %s, %s)",
                (str(review.reviewID), str(review.userID), str(review.hotelID), review.rating, review.comment)
            )
        except psycopg2.errors.ForeignKeyViolation as e:
            logging.exception(e)
            cursor.connection.rollback()

            if 'user_id' in str(e):
                raise HTTPException(status_code=404, detail="User ID not found.")

            if 'hotel_id' in str(e):
                raise HTTPException(status_code=404, detail="Hotel ID not found.")

            raise HTTPException(status_code=400, detail="Foreign key constraint violation.")
