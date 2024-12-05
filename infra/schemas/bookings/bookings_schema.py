from pydantic import BaseModel

class Booking(BaseModel):
    id: int
    date: str
    hour: str
    car: str
    client: str