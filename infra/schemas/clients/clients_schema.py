from pydantic import BaseModel

class Client(BaseModel):
    id: int
    firstName: str
    phone: str