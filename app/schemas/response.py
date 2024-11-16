from typing import List

from pydantic import BaseModel


class UserResponse(BaseModel):
    userID: str
    username: str
    email: str


class UsersResponse(BaseModel):
    users: List[UserResponse]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str


class RegisterResponse(BaseModel):
    message: str
    access_token: str
    user_id: str


class HotelResponse(BaseModel):
    hotel_id: str
    name: str
    address: str
