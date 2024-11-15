from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hashed(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    if not pwd_context.verify(plain_password, hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
