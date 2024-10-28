import uuid

from dataclasses import dataclass


@dataclass
class Hotel:
    hotelID: uuid.UUID
    name: str
    address: str
