import logging

from fastapi import HTTPException, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from app import env
from app.data.repository import user_repository
from app.di.dependencies import get_user_repository
from app.models.user import User
from app.routers import router
from app.routers.schemas.schemas import LoginBody, RegisterBody
from app.utils.jwt_util import create_access_token, get_current_user
from app.utils.password_util import *


@router.get("/users")
async def get_users(db: user_repository.UserRepository = Depends(get_user_repository),
                    current_user: User = Depends(get_current_user)):
    try:
        users = await db.get_all_users()
        template = env.get_template('user_list.html')
        return HTMLResponse(content=template.render(users=users))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/login", response_class=HTMLResponse)
async def show_login_page():
    template = env.get_template('login.html')
    return HTMLResponse(content=template.render())


@router.post("/token")
async def login(response: Response,
                user: LoginBody = Depends(LoginBody.as_form),
                db: user_repository.UserRepository = Depends(get_user_repository), ):
    existing_user = await db.retrieve_user_with_email(user.email)

    if not existing_user:
        raise HTTPException(status_code=404, detail="Account does not exist")

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(existing_user.userID)
    logging.debug(access_token)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return RedirectResponse(url="/users", status_code=303)


@router.get("/register", response_class=HTMLResponse)
async def show_register_page():
    template = env.get_template('register.html')
    return HTMLResponse(content=template.render())


@router.post("/register")
async def register(response: Response,
                   user: RegisterBody = Depends(RegisterBody.as_form),
                   db: user_repository.UserRepository = Depends(get_user_repository)):
    try:
        existing_user = await db.retrieve_user_with_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Account already exists")

        await db.create_user(username=user.username, email=user.email,
                             password=get_password_hashed(user.password))

        # Retrieve the newly created user to generate a token
        new_account = await db.retrieve_user_with_email(user.email)
        access_token = create_access_token(new_account.userID)

        # Set the token in a cookie
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return RedirectResponse(url="/users", status_code=303)
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail="Server side error, please contact administrator")
