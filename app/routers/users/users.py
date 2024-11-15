from fastapi import Depends, Response

from app.routers.users import router
from app.schemas.request import LoginBody, RegisterBody
from app.schemas.response import TokenResponse, RegisterResponse
from app.services.user_service import UserService


@router.post("/token", response_model=TokenResponse)
async def login(response: Response, user: LoginBody, service: UserService = Depends(UserService)):
    token_response = await service.login(user)
    response.set_cookie(key="access_token", value=f"Bearer {token_response.access_token}", httponly=True)
    return token_response


@router.post("/register", response_model=RegisterResponse)
async def register(user: RegisterBody, service: UserService = Depends(UserService)):
    return await service.register(user)
