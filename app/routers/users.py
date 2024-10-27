from typing import Annotated

from fastapi import Body, HTTPException
from pydantic import BaseModel, Field

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
        user_repository.create_user()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
