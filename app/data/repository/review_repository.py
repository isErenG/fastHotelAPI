import uuid
from typing import List, Optional

from typing_extensions import override

from app.data.repository import cursor
from app.models.repository.review_repository_abs import ReviewRepositoryInterface
from app.models.review import Review


class ReviewRepository(ReviewRepositoryInterface):
    def __init__(self):
        super().__init__()

    @override
    async def get_all_reviews(self) -> List[Review]:
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

    @override
    async def get_all_reviews_for_user(self, user_id: uuid.UUID) -> List[Review]:
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

    @override
    async def get_reviews_for_hotel(self, hotel_id: uuid.UUID) -> List[Review]:
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

    @override
    async def retrieve_review(self, review_id: uuid.UUID) -> Optional[Review]:
        cursor.execute("SELECT * FROM reviews WHERE review_id = %s", (str(review_id),))
        row = cursor.fetchone()

        if row:
            return Review(review_id=row[0],
                          user_id=row[1],
                          hotel_id=row[2],
                          rating=row[3],
                          comment=row[4])

    @override
    async def upload_review(self, review: Review):
        cursor.execute(
            "INSERT INTO reviews (user_id, hotel_id, rating, comment) VALUES (%s, %s, %s, %s)",
            (str(review.user_id), str(review.hotel_id), review.rating, review.comment)
        )
        cursor.connection.commit()

    @override
    async def delete_review(self, review_id: uuid.UUID):
        cursor.execute("DELETE FROM reviews WHERE review_id = %s", (str(review_id),))
        cursor.connection.commit()
