import uuid

from dataclasses import dataclass


@dataclass
class Review:
    review_id: uuid.UUID
    user_id: uuid.UUID
    hotel_id: uuid.UUID
    rating: int
    comment: str
