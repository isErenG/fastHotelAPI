import logging

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
        self.logger = logging.getLogger(__name__)

    async def _get_user_db(self) -> UserRepositoryInterface:
        if self.user_db is None:
            self.logger.debug("Initializing user repository")
            self.user_db = await get_user_repository()
        return self.user_db

    async def login(self, user_data: LoginBody):
        self.logger.info(f"User login attempt: {user_data.email}")
        db = await self._get_user_db()

        existing_user = await db.retrieve_user_with_email(user_data.email)
        if not existing_user:
            self.logger.warning(f"Login failed: Account does not exist for email {user_data.email}")
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Account does not exist")

        if not verify_password(user_data.password, existing_user.password):
            self.logger.warning(f"Login failed: Incorrect password for email {user_data.email}")
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        self.logger.info(f"User {user_data.email} logged in successfully")
        access_token = create_access_token(user_id=existing_user.user_id, is_admin=False)
        return TokenResponse(access_token=access_token, token_type="bearer", user_id=str(existing_user.user_id))

    async def register(self, user_data: RegisterBody):
        self.logger.info(f"User registration attempt: {user_data.email}")
        db = await self._get_user_db()

        try:
            await db.retrieve_user_with_email(user_data.email)
            self.logger.warning(f"Registration failed: Email {user_data.email} is already in use")
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Email is already in use")
        except HTTPException as e:
            if e.status_code != HTTP_404_NOT_FOUND:
                raise e

        await db.create_user(username=user_data.username, email=user_data.email,
                             password=get_password_hashed(user_data.password))
        self.logger.info(f"User {user_data.email} registered successfully")

        new_account = await db.retrieve_user_with_email(user_data.email)
        access_token = create_access_token(user_id=new_account.user_id, is_admin=False)

        self.logger.debug(f"Access token created for user {user_data.email}")
        return RegisterResponse(
            message="Account created successfully",
            access_token=access_token,
            user_id=str(new_account.user_id)
        )
