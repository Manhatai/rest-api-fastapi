from pydantic import BaseModel
from typing import Optional

class BookingSchema(BaseModel):
    id: Optional[int] = None
    date: str
    hour: str
    car: str
    client: str