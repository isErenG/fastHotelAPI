import uuid
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.data.repository.user_repository import UserRepository
from app.di.dependencies import get_user_repository
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


def create_access_token(data: uuid.UUID, expires_delta: int = None) -> str:
    expires_delta = calculate_expires_delta(expires_delta, Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": {"id": data}}
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: int = None) -> str:
    expires_delta = calculate_expires_delta(expires_delta, Config.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(data)}
    encoded_jwt = jwt.encode(to_encode, Config.JWT_REFRESH_SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


def calculate_expires_delta(expires_delta, expire_duration):
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=expire_duration)
    return expires_delta


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: UserRepository = Depends(get_user_repository)):
    return await db.retrieve_user_with_id(verify_token(token)["sub"]["id"])
