import os

from dotenv import load_dotenv
from pydantic.dataclasses import dataclass

load_dotenv(dotenv_path='.env')


@dataclass
class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY', 'golangconstructor')
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
    ALGORITHM = "HS256"
