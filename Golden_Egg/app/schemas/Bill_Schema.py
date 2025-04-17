from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class BillBase(BaseModel):
    issueDate: date
    totalPrice: float
    paid: bool

    class Config:
        from_attributes = True

class BillCreate(BillBase):
    order_id: int

class BillUpdate(BaseModel):
    issueDate: Optional[date] = None
    totalPrice: Optional[float] = None
    paid: Optional[bool] = None
    order_id: Optional[int] = None

    class Config:
        from_attributes = True

class Bill(BillBase):
    id: int
    order_id: int
    order: Optional["Order"] = None
    pays: List["Pay"] = []

    class Config:
        from_attributes = True