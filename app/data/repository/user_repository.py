import uuid
from typing import List

from typing_extensions import override

from app.data.repository import conn, cursor
from app.models.repository.user_repository_abs import UserRepositoryInterface
from app.models.user import User


class UserRepository(UserRepositoryInterface):
    def __init__(self):
        super().__init__()

    @override
    async def get_all_users(self) -> List[User]:
        user_list = []

        cursor.execute("SELECT * FROM users")

        results = cursor.fetchall()

        for row in results:
            user_list.append(User(row[0], row[1], row[2]))

        return user_list

    @override
    async def retrieve_user(self, user_id: uuid.UUID) -> User:
        return user_id

    @override
    async def create_user(self, user: User):
        return user
