from http.client import HTTPResponse
from typing import Annotated

from fastapi import Body, HTTPException
from pydantic import BaseModel, Field

from app.models.user import User
from app.routers import router, user_repository


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


@router.post("/users")
async def create_user(user: UserBody):
    try:
        await user_repository.create_user(username=user.username, email=user.email, password=user.password)
        return {"status": "account created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
