from pydantic import BaseModel
from typing import List, Optional

class TypeEggCreate(BaseModel):
    type: str

class TypeEggResponse(BaseModel):
    id: int
    type: str
    suppliers: Optional[List] = []

    class Config:
        orm_mode = True
