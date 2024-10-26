import uuid

from dataclasses import dataclass
from typing import List


@dataclass
class Hotel:
    hotelID: uuid.UUID
    name: str
    address: str
    management: List[uuid.UUID]