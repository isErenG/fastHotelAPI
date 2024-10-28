import uuid

from app.models.user import User


def map_to_model(user_id: uuid.UUID, name: str, email: str) -> User:
    return User(userID=user_id, username=name, email=email)