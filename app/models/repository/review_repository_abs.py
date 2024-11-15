import uuid
from abc import ABC, abstractmethod
from typing import List

from app.models.review import Review


class ReviewRepositoryInterface(ABC):

    @abstractmethod
    async def get_all_reviews(self) -> List[Review]:
        pass

    @abstractmethod
    async def get_all_reviews_for_user(self, user_id: uuid.UUID) -> List[Review]:
        pass

    @abstractmethod
    async def get_reviews_for_hotel(self, hotel_id: uuid.UUID) -> List[Review]:
        pass

    @abstractmethod
    async def retrieve_review(self, review_id: uuid.UUID) -> Review:
        pass

    @abstractmethod
    async def upload_review(self, review: Review):
        pass

    @abstractmethod
    async def delete_review(self, review_id: uuid.UUID):
        pass
