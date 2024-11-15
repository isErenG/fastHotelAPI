import uuid

from fastapi import Depends, Path, HTTPException
from starlette.responses import JSONResponse, Response

from app.data.repository import user_repository, admin_repository
from app.di.dependencies import get_user_repository, get_admin_repository
from app.models.admin import Admin
from app.routers.admin import admin_router
from app.schemas.request import LoginBody, UpdateUserRequest
from app.schemas.response import UsersResponse, UserResponse, TokenResponse
from app.utils.admin_dependency import admin_dependency
from app.utils.jwt_helper import create_access_token
from app.utils.password_util import verify_password


@admin_router.get("/users", response_model=UsersResponse, tags=["admin"])
async def get_users(
        db: user_repository.UserRepository = Depends(get_user_repository),
        current_user: Admin = Depends(admin_dependency),
):
    if not isinstance(current_user, Admin):
        raise HTTPException(status_code=403, detail="Forbidden access")

    users = await db.get_all_users()
    user_data = [UserResponse(userID=str(user.user_id), username=user.username, email=user.email) for user in users]
    return JSONResponse(content=UsersResponse(users=user_data).dict())


@admin_router.delete("/users/{user_id}", tags=["admin"])
async def delete_user(
        user_id: uuid.UUID = Path(..., description="The ID of the user to delete"),
        db: user_repository.UserRepository = Depends(get_user_repository),
        current_user: Admin = Depends(admin_dependency),
):
    if not isinstance(current_user, Admin):
        raise HTTPException(status_code=403, detail="Forbidden access")

    user = await db.retrieve_user_with_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete_user(user_id)
    return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)


@admin_router.put("/users/{user_id}", response_model=UserResponse, tags=["admin"])
async def update_user(
        user_data: UpdateUserRequest,
        user_id: uuid.UUID = Path(..., description="The ID of the user to update"),
        db: user_repository.UserRepository = Depends(get_user_repository),
        current_user: Admin = Depends(admin_dependency),
):
    user = await db.retrieve_user_with_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.username:
        user.username = user_data.username
    if user_data.email:
        user.email = user_data.email

    await db.update_user(user)

    return UserResponse(user_id=str(user.user_id), username=user.username, email=user.email)


@admin_router.post("/token", response_model=TokenResponse, tags=["admin"])
async def admin_login(
        response: Response,
        login_data: LoginBody,
        db: admin_repository.AdminRepository = Depends(get_admin_repository),
):
    admin = await db.get_admin_by_email(login_data.email)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin account not found")

    if not verify_password(login_data.password, admin.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(user_id=admin.admin_id, is_admin=True)

    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

    return TokenResponse(access_token=access_token, token_type="bearer", user_id=str(admin.admin_id))
