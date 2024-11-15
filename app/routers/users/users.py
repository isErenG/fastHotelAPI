from fastapi import Depends, Response
from fastapi.responses import JSONResponse

from app.data.repository import user_repository
from app.di.dependencies import get_user_repository
from app.routers.users import router
from app.schemas.request import LoginBody, RegisterBody
from app.schemas.response import TokenResponse, RegisterResponse
from app.utils.jwt_helper import create_access_token
from app.utils.password_util import *


@router.post("/token", response_model=TokenResponse)
async def login(response: Response,
                user: LoginBody,
                db: user_repository.UserRepository = Depends(get_user_repository)):
    existing_user = await db.retrieve_user_with_email(user.email)

    verify_password(user.password, existing_user.password)

    access_token = create_access_token(user_id=existing_user.user_id, is_admin=False)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return JSONResponse(
        content=TokenResponse(access_token=access_token, token_type="bearer",
                              user_id=str(existing_user.user_id)).dict())


@router.post("/register", response_model=RegisterResponse)
async def register(user: RegisterBody,
                   db: user_repository.UserRepository = Depends(get_user_repository)):
    await db.create_user(username=user.username, email=user.email,
                         password=get_password_hashed(user.password))

    new_account = await db.retrieve_user_with_email(user.email)
    access_token = create_access_token(user_id=new_account.user_id, is_admin=False)

    return JSONResponse(content=RegisterResponse(
        message="Account created successfully",
        access_token=access_token,
        user_id=str(new_account.user_id)
    ))
