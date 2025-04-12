from pydantic import BaseModel
from datetime import date

class InventoryBase(BaseModel):
    nameProduct: str
    entryDate: date
    expirationDate: date
    totalPrice: float
    quantity: int
    
class InventoryCreate(InventoryBase):
    pass


class InventoryResponse(InventoryBase):
    id: int
    class Config:
        orm_mode = True