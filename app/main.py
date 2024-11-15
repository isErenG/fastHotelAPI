import logging

from fastapi import FastAPI

from app.middleware.logging import LoggingMiddleware
from app.routers.admin import users as admin_users
from app.routers.users import hotels, reviews, users
from app.utils.config import Config

app = FastAPI()

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))

app.add_middleware(LoggingMiddleware)

app.include_router(users.router, tags=["users"])
app.include_router(hotels.router, tags=["hotels"])
app.include_router(reviews.router, tags=["reviews"])
app.include_router(admin_users.admin_router, tags=["admin"])
