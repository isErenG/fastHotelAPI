import uuid
from dataclasses import dataclass


@dataclass
class User:
    user_id: uuid.UUID
    username: str
    email: str
    password: str

