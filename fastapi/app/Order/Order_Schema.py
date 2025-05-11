from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi.app.User.user_schema import *

class OrderBase(BaseModel):
    totalPrice: float
    orderDate: date
    state: str
    user_id: int

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True