from typing import Annotated

from fastapi import Body, HTTPException
from pydantic import BaseModel, Field

from app.data.user_repository import UserRepository
from app.routers import router


@router.get("/users")
async def get_users():
    await UserRepository.retrieve_user()
    return {"users": "user"}


class User(BaseModel):
    username: str
    email: str
    password: str


@router.post("/users")
async def create_user(
        user: User
):
    try:
        await UserRepository.create_user(user)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
