from pydantic import BaseModel
from typing import Optional

class CarSchema(BaseModel):
    id: Optional[int] = None
    brand: str
    model: str
    year: str
    malfunction: str