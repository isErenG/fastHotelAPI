from fastapi import FastAPI
from .routers import hotels
from .routers import users

# Golang constructor
app = FastAPI()
app.include_router(hotels.router)
app.include_router(users.router)
