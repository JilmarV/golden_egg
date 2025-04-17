from pydantic import BaseModel
from typing import Optional, List

class EggBase(BaseModel):
    color: str
    price: float

    class Config:
        from_attributes = True

class EggCreate(EggBase):
    type_id: int

class EggUpdate(BaseModel):
    color: Optional[str] = None
    price: Optional[float] = None
    type_id: Optional[int] = None

    class Config:
        from_attributes = True

class Egg(EggBase):
    id: int
    type_id: int
    type: Optional["TypeEgg"] = None
    inventory: Optional["Inventory"] = None
    orders: List["Order"] = []

    class Config:
        from_attributes = True