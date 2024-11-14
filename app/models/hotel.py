import uuid

from dataclasses import dataclass


@dataclass
class Hotel:
    hotel_id: uuid.UUID
    name: str
    address: str
