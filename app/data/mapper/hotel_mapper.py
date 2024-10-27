import uuid

from app.models.hotel import Hotel


def map_to_model(hotel_id: uuid.UUID, name: str, address: str) -> Hotel:
    return Hotel(hotel_id, name, address)