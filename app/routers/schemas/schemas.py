from typing import Optional

from pydantic import BaseModel


class UserBody(BaseModel):
    username: str
    email: str
    password: str


class HotelBody(BaseModel):
    name: str
    address: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[str] = None
