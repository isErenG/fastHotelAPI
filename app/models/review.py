import uuid
from dataclasses import dataclass

@dataclass
class Review:
    userID: uuid.UUID
    hotelID: uuid.UUID
    rating: int
    comment: str