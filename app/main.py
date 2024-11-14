import logging

from fastapi import FastAPI

from app.routers import users
from app.routers.admin import admin_router
from .middleware.admin_auth import AdminOnlyMiddleware
from .middleware.logging import LoggingMiddleware
from .routers.users import hotels, reviews
from .utils.config import Config

app = FastAPI()

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))

app.add_middleware(LoggingMiddleware)
app.add_middleware(AdminOnlyMiddleware)

app.include_router(admin_router)
app.include_router(hotels.router)
app.include_router(users.router)
app.include_router(reviews.router)
