from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.User.User_Schema import *

class OrderEggBase(BaseModel):
    quantity: int
    unit_price: float
    unit_price: float
    sub_total: float
    egg_id: int
    order_id: int

class OrderEggCreate(OrderEggBase):
    pass

class OrderEggResponse(OrderEggBase):
    id: int

    class Config:
        from_attributes = True