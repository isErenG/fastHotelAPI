import uuid

from dataclasses import dataclass


@dataclass
class Review:
    reviewID: uuid.UUID
    userID: uuid.UUID
    hotelID: uuid.UUID
    rating: int
    comment: str
