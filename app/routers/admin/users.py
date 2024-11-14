import uuid

from fastapi import Depends, Path, Body, HTTPException
from starlette.responses import JSONResponse

from app.data.repository import user_repository
from app.di.dependencies import get_user_repository
from app.models.admin import Admin
from app.models.user import User
from app.routers.admin import admin_router
from app.schemas.response import UsersResponse, UserResponse
from app.utils.jwt_helper import get_current_user


@admin_router.get("/users", response_model=UsersResponse, tags=["admin"])
async def get_users(db: user_repository.UserRepository = Depends(get_user_repository),
                    current_user: Admin = Depends(get_current_user)):
    if not isinstance(current_user, Admin):
        raise HTTPException(status_code=403, detail="Forbidden access")

    users = await db.get_all_users()
    user_data = [UserResponse(userID=str(user.user_id), username=user.username, email=user.email) for user in users]
    return JSONResponse(content=UsersResponse(users=user_data).dict())


@admin_router.delete("/users/{user_id}", tags=["admin"])
async def delete_user(user_id: uuid.UUID = Path(..., description="The ID of the user to delete"),
                      db: user_repository.UserRepository = Depends(get_user_repository),
                      current_user: User = Depends(get_current_user)):
    if not isinstance(current_user, Admin):
        raise HTTPException(status_code=403, detail="Forbidden access")

    user = await db.retrieve_user_with_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete_user(user_id)
    return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)


@admin_router.put("/users/{user_id}", response_model=UserResponse, tags=["admin"])
async def update_user(user_id: str = Path(..., description="The ID of the user to update"),
                      username: str = Body(None, description="New username for the user"),
                      email: str = Body(None, description="New email for the user"),
                      db: user_repository.UserRepository = Depends(get_user_repository),
                      current_user: User = Depends(get_current_user)):
    if not isinstance(current_user, Admin):
        raise HTTPException(status_code=403, detail="Forbidden access")

    user = await db.retrieve_user_with_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if username:
        user.username = username
    if email:
        user.email = email

    await db.update_user(user)

    return JSONResponse(content=UserResponse(userID=str(user.user_id), username=user.username, email=user.email).dict())
