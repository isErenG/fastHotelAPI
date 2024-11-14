from fastapi import HTTPException, Depends, Response
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
                user: LoginBody = Depends(LoginBody.as_form),
                db: user_repository.UserRepository = Depends(get_user_repository)):
    existing_user = await db.retrieve_user_with_email(user.email)

    if not existing_user:
        raise HTTPException(status_code=404, detail="Account does not exist")

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(existing_user.user_id)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return JSONResponse(
        content=TokenResponse(access_token=access_token, token_type="bearer", user_id=str(existing_user.user_id)).dict())


@router.post("/register", response_model=RegisterResponse)
async def register(user: RegisterBody = Depends(RegisterBody.as_form),
                   db: user_repository.UserRepository = Depends(get_user_repository)):
    existing_user = await db.retrieve_user_with_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Account already exists")

    await db.create_user(username=user.username, email=user.email,
                         password=get_password_hashed(user.password))

    # Retrieve the newly created user to generate a token
    new_account = await db.retrieve_user_with_email(user.email)
    access_token = create_access_token(new_account.user_id)

    return JSONResponse(content=RegisterResponse(
        message="Account created successfully",
        access_token=access_token,
        user_id=str(new_account.user_id)
    ))
