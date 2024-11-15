from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LoginBody(BaseModel):
    email: EmailStr = Field(..., description="The user's email address, validated as an email format.")
    password: str = Field(..., min_length=8, description="The user's password with a minimum length of 8 characters.")


class UpdateUserRequest(BaseModel):
    username: Optional[str] = Field(None, description="Updated username")
    email: Optional[EmailStr] = Field(None, description="Updated email address")


class RegisterBody(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="The user's unique username.")
    email: EmailStr = Field(..., description="The user's email address, validated as an email format.")
    password: str = Field(..., min_length=8, description="The user's password with a minimum length of 8 characters.")


class CreateHotelBody(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The hotel's name.")
    address: str = Field(..., min_length=1, max_length=200, description="The hotel's address.")


class TokenData(BaseModel):
    sub: Optional[str] = Field(None, description="The subject identifier, usually the user ID or username.")
