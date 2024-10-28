from fastapi import HTTPException
from pydantic import BaseModel

from app.routers import router, user_repository
from app.utils.password_util import *


@router.get("/users")
async def get_users():
    try:
        return await user_repository.get_all_users()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class UserBody(BaseModel):
    username: str
    email: str
    password: str


@router.post("/login")
async def login(user: UserBody):
    try:
        existing_user = await user_repository.retrieve_user_with_email(user.email)

        if not existing_user:
            # Give a better response
            return {"error": "account does not exist"}

        if verify_password(user.password, existing_user.password):
            # Give a better response
            return {"success": True}

        return {"success": False}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register")
async def register(user: UserBody):
    try:
        existing_user = await user_repository.retrieve_user_with_email(user.email)

        if existing_user:
            # Give a better response
            return {"error": "account exists"}

        await user_repository.create_user(username=user.username, email=user.email,
                                          password=get_password_hashed(user.password))

        return {"success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
