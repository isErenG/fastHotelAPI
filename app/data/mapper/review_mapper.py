import uuid

from app.models.review import Review


def map_to_modal(review_id: uuid.UUID, user_id: uuid.UUID, hotel_id: uuid.UUID, rating: int, comment: str) -> Review:
    return Review(
        reviewID=review_id,
        userID=user_id,
        hotelID=hotel_id,
        rating=rating,
        comment=comment
    )
