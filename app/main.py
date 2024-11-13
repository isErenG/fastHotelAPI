import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .middleware.logging import LoggingMiddleware
from .routers import hotels
from .routers import reviews
from .routers import users
from .utils.config import Config

app = FastAPI()

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL, logging.INFO))

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)
app.include_router(hotels.router)
app.include_router(users.router)
app.include_router(reviews.router)
