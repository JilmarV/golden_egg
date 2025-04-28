from pydantic import BaseModel
from typing import Optional
from datetime import date
from Order.Order_Schema import OrderResponse
#from Egg.Egg_Schema import EggResponse

class OrderEggBase(BaseModel):
    order_id: int
    egg_id: int

class OrderEggCreate(OrderEggBase):
    pass

class OrderEggResponse(OrderEggBase):
    id: int
    order: Optional[OrderResponse] = None
    #egg: Optional[EggResponse] = None

    class Config:
        from_attributes = True