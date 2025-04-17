from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class OrderBase(BaseModel):
    totalPrice: float
    orderDate: date
    state: str

    class Config:
        from_attributes = True


class OrderCreate(OrderBase):
    egg_ids: List[int] = []


class OrderUpdate(BaseModel):
    totalPrice: Optional[float] = None
    orderDate: Optional[date] = None
    state: Optional[str] = None
    egg_ids: Optional[List[int]] = None

    class Config:
        from_attributes = True


class Order(OrderBase):
    id: int
    eggs: List["Egg"] = []
    bill: Optional["Bill"] = None

    class Config:
        from_attributes = True