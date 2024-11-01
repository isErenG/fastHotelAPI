import logging

from fastapi import FastAPI

from .middleware.logging import LoggingMiddleware
from .routers import hotels
from .routers import users
from .utils.config import Config

app = FastAPI()

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL, logging.INFO))

app.add_middleware(LoggingMiddleware)
app.include_router(hotels.router)
app.include_router(users.router)
