import logging
import uuid
from datetime import datetime, timedelta
from typing import Union

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.data.repository.admin_repository import AdminRepository
from app.data.repository.user_repository import UserRepository
from app.di.dependencies import get_user_repository, get_admin_repository
from app.models.admin import Admin
from app.models.user import User
from app.utils.config import Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str):
    try:
        decoded_token = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def create_access_token(user_id: uuid.UUID, is_admin: bool, expires_delta: int = None) -> str:
    expires_delta = calculate_expires_delta(expires_delta, Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expires_delta,
        "sub": {
            "id": user_id,
            "is_admin": is_admin
        }
    }
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: uuid.UUID, is_admin: bool, expires_delta: int = None) -> str:
    expires_delta = calculate_expires_delta(expires_delta, Config.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expires_delta,
        "sub": {
            "id": str(user_id),
            "is_admin": is_admin
        }
    }
    encoded_jwt = jwt.encode(to_encode, Config.JWT_REFRESH_SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


def calculate_expires_delta(expires_delta, expire_duration):
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=expire_duration)
    return expires_delta


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_db: UserRepository = Depends(get_user_repository),
        admin_db: AdminRepository = Depends(get_admin_repository)
) -> Union[User, Admin]:
    decoded_token = verify_token(token)
    user_id = decoded_token["sub"]["id"]
    is_admin = decoded_token["sub"]["is_admin"]

    if is_admin:
        admin_user = await admin_db.get_admin(user_id)
        if admin_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin user not found")
        return admin_user

    user = await user_db.retrieve_user_with_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

