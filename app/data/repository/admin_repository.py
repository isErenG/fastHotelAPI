import uuid
from datetime import date
from typing import Optional

from fastapi import HTTPException

from app.data.repository import cursor
from app.models.admin import Admin
from app.models.repository.admin_repository_abs import AdminRepositoryInterface


class AdminRepository(AdminRepositoryInterface):
    def __init__(self):
        super().__init__()

    async def create_admin(self, name: str, email: str, password: str, start_date: date, end_date: date) -> Admin:
        cursor.execute(
            """
            INSERT INTO admins (name, email, password, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s) RETURNING admin_id
            """,
            (name, email, password, start_date, end_date)
        )

        admin_id = uuid.UUID(cursor.fetchone()[0])

        cursor.connection.commit()

        return Admin(user_id=admin_id, username=name, email=email, password=password, start_date=start_date,
                     end_date=end_date)

    async def get_admin(self, admin_id: uuid.UUID) -> Optional[Admin]:
        cursor.execute("SELECT * FROM admins WHERE admin_id = %s", (str(admin_id),))
        row = cursor.fetchone()

        if row:
            return Admin(user_id=row[0], username=row[1], email=row[2], password=row[3], start_date=row[4],
                         end_date=row[5])

        return None

    async def remove_admin(self, admin_id: uuid.UUID) -> None:
        cursor.execute("DELETE FROM admins WHERE admin_id = %s", (str(admin_id),))

        cursor.connection.commit()

    async def update_admin(self, admin_id: uuid.UUID, name: Optional[str] = None, email: Optional[str] = None,
                           password: Optional[str] = None, start_date: Optional[date] = None,
                           end_date: Optional[date] = None) -> Optional[Admin]:
        updates = []
        values = []

        if name:
            updates.append("name = %s")
            values.append(name)
        if email:
            updates.append("email = %s")
            values.append(email)
        if password:
            updates.append("password = %s")
            values.append(password)
        if start_date:
            updates.append("start_date = %s")
            values.append(start_date)
        if end_date:
            updates.append("end_date = %s")
            values.append(end_date)

        if not updates:
            return None

        values.append(str(admin_id))
        update_query = ", ".join(updates)

        cursor.execute(
            f"UPDATE admins SET {update_query} WHERE admin_id = %s",
            tuple(values)
        )

        cursor.connection.commit()

        return await self.get_admin(admin_id)

    async def get_admin_by_email(self, email: str) -> Admin:
        cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
        row = cursor.fetchone()

        if row:
            return Admin(user_id=row[0], username=row[1], email=row[2], password=row[3], start_date=row[4],
                         end_date=row[5])

