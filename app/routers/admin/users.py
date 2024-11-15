import uuid

from fastapi import Depends, Path
from starlette.responses import JSONResponse

from app.models.admin import Admin
from app.routers.admin import admin_router
from app.schemas.request import LoginBody, UpdateUserRequest
from app.schemas.response import UsersResponse, UserResponse, TokenResponse
from app.services.admin_service import AdminService
from app.utils.admin_dependency import admin_dependency


@admin_router.get("/users", response_model=UsersResponse, tags=["admin"])
async def get_users(
        service: AdminService = Depends(AdminService),
        current_user: Admin = Depends(admin_dependency),
):
    return UsersResponse(users=await service.get_users())


@admin_router.delete("/users/{user_id}", tags=["admin"])
async def delete_user(
        user_id: uuid.UUID = Path(..., description="The ID of the user to delete"),
        service: AdminService = Depends(AdminService),
        current_user: Admin = Depends(admin_dependency),
):
    await service.delete_user(user_id)
    return JSONResponse(content={"status": "success"})


@admin_router.put("/users/{user_id}", response_model=UserResponse, tags=["admin"])
async def update_user(
        user_data: UpdateUserRequest,
        user_id: uuid.UUID = Path(..., description="The ID of the user to update"),
        service: AdminService = Depends(AdminService),
        current_user: Admin = Depends(admin_dependency),
):
    return await service.update_user(user_id, user_data)


@admin_router.post("/token", response_model=TokenResponse, tags=["admin"])
async def admin_login(
        login_data: LoginBody,
        service: AdminService = Depends(AdminService),
):
    return await service.get_token(login_data)
