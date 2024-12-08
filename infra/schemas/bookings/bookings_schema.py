from pydantic import BaseModel
from typing import Optional
from infra.schemas.cars.cars_schema import CarSchema
from infra.schemas.clients.clients_schema import ClientSchema

class BookingSchema(BaseModel):
    id: Optional[int] = None
    date: str
    hour: str
    car_id: int
    car: Optional[CarSchema] = None
    client_id: int
    client: Optional[ClientSchema] = None