from typing import Optional

from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.di.dependencies import get_user_repository, get_admin_repository
from app.models.repository.admin_repository_abs import AdminRepositoryInterface
from app.models.repository.user_repository_abs import UserRepositoryInterface
from app.schemas.request import UpdateUserRequest, LoginBody
from app.schemas.response import UserResponse, TokenResponse
from app.utils.jwt_helper import create_access_token
from app.utils.password_util import verify_password


class AdminService:
    def __init__(self):
        self.user_db: Optional[UserRepositoryInterface] = None
        self.admin_db: Optional[AdminRepositoryInterface] = None

    async def _get_user_db(self) -> UserRepositoryInterface:
        if self.user_db is None:
            self.user_db = await get_user_repository()
        return self.user_db

    async def _get_admin_db(self) -> AdminRepositoryInterface:
        if self.admin_db is None:
            self.admin_db = await get_admin_repository()
        return self.admin_db

    async def get_users(self):
        db = await self._get_user_db()
        users = await db.get_all_users()

        if not users:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No users found")

        return [UserResponse(userID=str(user.user_id), username=user.username, email=user.email) for user in users]

    async def delete_user(self, user_id):
        db = await self._get_user_db()

        user = await db.retrieve_user_with_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete_user(user_id)

    async def update_user(self, user_id, user_data: UpdateUserRequest):
        db = await self._get_user_db()

        user = await db.retrieve_user_with_id(user_id)

        if user_data.username:
            user.username = user_data.username
        if user_data.email:
            user.email = user_data.email

        await db.update_user(user)

        return UserResponse(userID=str(user.user_id), username=user.username, email=user.email)

    async def get_token(self, login_data: LoginBody):
        db = await self._get_admin_db()

        admin = await db.get_admin_by_email(login_data.email)

        if not verify_password(login_data.password, admin.password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        access_token = create_access_token(user_id=admin.admin_id, is_admin=True)

        return TokenResponse(access_token=access_token, token_type="bearer", user_id=str(admin.admin_id))
