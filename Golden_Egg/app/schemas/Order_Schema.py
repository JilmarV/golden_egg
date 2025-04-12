from pydantic import BaseModel
from datetime import date

class OrderBase(BaseModel):
    state: str
    orderDate: date
    totalPrice: float
    
class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    class Config:
        orm_mode = True