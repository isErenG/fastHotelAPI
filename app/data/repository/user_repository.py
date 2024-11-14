import uuid
from typing import List, Optional

from typing_extensions import override

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
            user_list.append(User(user_id=row[0], username=row[1], email=row[2], password=row[3]))

        return user_list

    @override
    async def retrieve_user_with_email(self, user_email: str) -> Optional[User]:
        cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))

        row = cursor.fetchone()

        if row:
            return User(user_id=row[0], username=row[1], email=row[2], password=row[3])
        return None

    @override
    async def retrieve_user_with_id(self, user_id: uuid.UUID) -> Optional[User]:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))

        row = cursor.fetchone()

        if row:
            return User(user_id=row[0], username=row[1], email=row[2], password=row[3])
        return None

    @override
    async def create_user(self, username: str, email: str, password: str):
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (username, email, password),
        )

        cursor.connection.commit()

    async def delete_user(self, user_id: uuid.UUID):
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

        cursor.connection.commit()

    async def update_user(self, updated_user: User):
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE user_id = %s",
                       (updated_user.username, updated_user.email, updated_user.user_id))

        cursor.connection.commit()
