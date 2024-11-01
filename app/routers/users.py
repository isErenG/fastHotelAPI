import logging

from fastapi import HTTPException, Depends

from app.data.repository import user_repository
from app.di.dependencies import get_user_repository
from app.models.user import User
from app.routers import router
from app.routers.schemas.schemas import UserBody, Token
from app.utils.jwt_util import create_access_token, get_current_user
from app.utils.password_util import *


@router.get("/users")
async def get_users(db: user_repository.UserRepository = Depends(get_user_repository),
                    current_user: User = Depends(get_current_user)):
    try:
        return await db.get_all_users()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token", response_model=Token)
async def login(user: UserBody,
                db: user_repository.UserRepository = Depends(get_user_repository)):
    try:
        existing_user = await db.retrieve_user_with_email(user.email)

        if not existing_user:
            return HTTPException(status_code=404, detail="account does not exist")

        if not verify_password(user.password, existing_user.password):
            return HTTPException(status_code=401, detail="incorrect email or password")

        access_token = create_access_token(existing_user.userID)

        return Token(access_token=access_token, token_type="bearer")


    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail="server side error, please contact administrator")


@router.post("/register")
async def register(user: UserBody,
                   db: user_repository.UserRepository = Depends(get_user_repository)):
    try:
        existing_user = await db.retrieve_user_with_email(user.email)

        if existing_user:
            return HTTPException(status_code=400, detail="account does already exists")

        await db.create_user(username=user.username, email=user.email,
                             password=get_password_hashed(user.password))

        # In order to retrieve the ID to pass to the token, I have to retrieve again
        # I admit this is dirty, I should return an ID from .create_user()
        new_account = await db.retrieve_user_with_email(user.email)

        return Token(access_token=new_account.userID, token_type="bearer")

    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail="server side error, please contact administrator")
