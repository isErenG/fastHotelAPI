from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.di.dependencies import get_user_repository
from app.models.repository.user_repository_abs import UserRepositoryInterface
from app.schemas.request import LoginBody, RegisterBody
from app.schemas.response import TokenResponse, RegisterResponse
from app.utils.jwt_helper import create_access_token
from app.utils.password_util import get_password_hashed, verify_password


class UserService:
    def __init__(self):
        self.user_db: UserRepositoryInterface = None

    async def _get_user_db(self) -> UserRepositoryInterface:
        if self.user_db is None:
            self.user_db = await get_user_repository()
        return self.user_db

    async def login(self, user_data: LoginBody):
        db = await self._get_user_db()
        existing_user = await db.retrieve_user_with_email(user_data.email)

        if not existing_user:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Account does not exist")

        if not verify_password(user_data.password, existing_user.password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        access_token = create_access_token(user_id=existing_user.user_id, is_admin=False)
        return TokenResponse(access_token=access_token, token_type="bearer", user_id=str(existing_user.user_id))

    async def register(self, user_data: RegisterBody):
        db = await self._get_user_db()

        try:
            await db.retrieve_user_with_email(user_data.email)
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Email is already in use")
        except HTTPException as e:
            if e.status_code != HTTP_404_NOT_FOUND:
                raise e

        await db.create_user(username=user_data.username, email=user_data.email,
                             password=get_password_hashed(user_data.password))

        new_account = await db.retrieve_user_with_email(user_data.email)
        access_token = create_access_token(user_id=new_account.user_id, is_admin=False)

        return RegisterResponse(
            message="Account created successfully",
            access_token=access_token,
            user_id=str(new_account.user_id)
        )
