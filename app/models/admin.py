import uuid
from dataclasses import dataclass
from datetime import date

@dataclass
class Admin:
    admin_id: uuid.UUID
    username: str
    email: str
    password: str
    start_date: date
    end_date: date
