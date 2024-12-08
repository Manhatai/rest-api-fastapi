from pydantic import BaseModel
from typing import Optional
class ClientSchema(BaseModel):
    id: Optional[int] = None #https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage
    firstName: str
    phone: str