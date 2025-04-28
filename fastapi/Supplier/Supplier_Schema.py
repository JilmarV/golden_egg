from pydantic import BaseModel
from typing import List, Optional

class SupplierCreate(BaseModel):
    name: str
    address: str

class SupplierResponse(BaseModel):
    id: int
    name: str
    address: str
    eggs: Optional[List] = []

    class Config:
        orm_mode = True
