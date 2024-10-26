import uuid

from typing_extensions import override

from app.models.repository.user_repository_abs import UserRepositoryInterface
from app.models.user import User


class UserRepository(UserRepositoryInterface):
    def __init__(self):
        super().__init__()

    @override
    async def retrieve_user(self, user_id: uuid.UUID):
        pass

    @override
    async def upload_user(self, user: User):
        pass
