import uuid
from typing import List, Optional

from typing_extensions import override

from app.data.mapper import user_mapper
from app.data.repository import cursor
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
            user_list.append(User(user_mapper.map_to_model(user_id=row[0], name=row[1], email=row[2])))

        return user_list

    @override
    async def retrieve_user(self, user_id: uuid.UUID) -> Optional[User]:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))

        row = cursor.fetchone()

        if row:
            return User(user_mapper.map_to_model(user_id, name=row[1], email=row[2]))
        return None

    @override
    async def create_user(self, username: str, email: str, password: str):
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (username, email)
        )

        cursor.connection.commit()
