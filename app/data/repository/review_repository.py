import uuid
from typing import List, Optional
from typing_extensions import override

from app.data.mapper import review_mapper
from app.data.repository import cursor
from app.models.review import Review
from app.models.repository.review_repository_abs import ReviewRepositoryInterface


class ReviewRepository(ReviewRepositoryInterface):
    def __init__(self):
        super().__init__()

    @override
    async def get_all_reviews(self) -> List[Review]:
        review_list = []
        cursor.execute("SELECT * FROM reviews")
        results = cursor.fetchall()

        for row in results:
            review_list.append(review_mapper.map_to_modal(review_id=row[0],
                                             user_id=row[1],
                                             hotel_id=row[2],
                                             rating=row[3],
                                             comment=row[4]))
        return review_list

    @override
    async def get_reviews_for_hotel(self, hotel_id: uuid.UUID) -> List[Review]:
        review_list = []
        cursor.execute("SELECT * FROM reviews WHERE hotel_id = %s", (hotel_id,))
        results = cursor.fetchall()

        for row in results:
            review_list.append(review_mapper.map_to_modal(review_id=row[0],
                                            user_id=row[1],
                                            hotel_id=row[2],
                                            rating=row[3],
                                            comment=row[4]))

        return review_list

    @override
    async def retrieve_review(self, review_id: uuid.UUID) -> Optional[Review]:
        cursor.execute("SELECT * FROM reviews WHERE review_id = %s", (review_id,))
        row = cursor.fetchone()

        if row:
            return review_mapper.map_to_modal(review_id=row[0],
                                user_id=row[1],
                                hotel_id=row[2],
                                rating=row[3],
                                comment=row[4])

        return None

    @override
    async def upload_review(self, review: Review):
        cursor.execute(
            "INSERT INTO reviews (review_id, user_id, hotel_id, rating, comment) VALUES (%s, %s, %s, %s, %s)",
            (review.reviewID, review.userID, review.hotelID, review.rating, review.comment)
        )
