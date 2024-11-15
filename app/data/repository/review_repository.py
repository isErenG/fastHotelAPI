import logging
import uuid
from typing import List

import psycopg2
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
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
            logging.exception("Error fetching all reviews.")
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Failed to fetch reviews.")

    @override
    async def get_all_reviews_for_user(self, user_id: uuid.UUID) -> List[Review]:
        try:
            review_list = []
            cursor.execute("SELECT * FROM reviews WHERE user_id = %s", (str(user_id),))
            results = cursor.fetchall()

            for row in results:
                review_list.append(Review(review_id=row[0],
                                          user_id=row[1],
                                          hotel_id=row[2],
                                          rating=row[3],
                                          comment=row[4]))
            return review_list
        except Exception as e:
            logging.exception(f"Error fetching reviews for user: {user_id}")
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Failed to fetch user reviews.")

    @override
    async def get_reviews_for_hotel(self, hotel_id: uuid.UUID) -> List[Review]:
        try:
            review_list = []
            cursor.execute("SELECT * FROM reviews WHERE hotel_id = %s", (str(hotel_id),))
            results = cursor.fetchall()

            for row in results:
                review_list.append(Review(review_id=row[0],
                                          user_id=row[1],
                                          hotel_id=row[2],
                                          rating=row[3],
                                          comment=row[4]))
            return review_list
        except Exception as e:
            logging.exception(f"Error fetching reviews for hotel: {hotel_id}")
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Failed to fetch hotel reviews.")

    @override
    async def retrieve_review(self, review_id: uuid.UUID) -> Review:
        try:
            cursor.execute("SELECT * FROM reviews WHERE review_id = %s", (str(review_id),))
            row = cursor.fetchone()

            if row:
                return Review(review_id=row[0],
                              user_id=row[1],
                              hotel_id=row[2],
                              rating=row[3],
                              comment=row[4])
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Review not found.")
        except Exception as e:
            logging.exception(f"Error fetching review: {review_id}")
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Failed to fetch review.")

    @override
    async def upload_review(self, review: Review):
        try:
            cursor.execute(
                "INSERT INTO reviews (review_id, user_id, hotel_id, rating, comment) VALUES (%s, %s, %s, %s, %s)",
                (str(review.review_id), str(review.user_id), str(review.hotel_id), review.rating, review.comment)
            )
            cursor.connection.commit()
        except psycopg2.errors.ForeignKeyViolation as e:
            logging.exception("Foreign key violation during review upload.")
            cursor.connection.rollback()

            if 'user_id' in str(e):
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User ID not found.")

            if 'hotel_id' in str(e):
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Hotel ID not found.")

            raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid review data.")
        except Exception as e:
            logging.exception("Error uploading review.")
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Failed to upload review.")

    @override
    async def delete_review(self, review_id: uuid.UUID):
        try:
            cursor.execute("DELETE FROM reviews WHERE review_id = %s", (str(review_id),))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Review not found.")
            cursor.connection.commit()
        except Exception as e:
            logging.exception(f"Error deleting review: {review_id}")
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete review.")
