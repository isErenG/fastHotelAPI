import uuid
from dataclasses import dataclass

@dataclass
class User:
    userID: uuid.UUID
    username: str
    email: str
    password: str