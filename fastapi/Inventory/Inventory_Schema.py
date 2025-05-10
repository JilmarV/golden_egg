from pydantic import BaseModel
from datetime import date

class InventoryBase(BaseModel):
    nameProduct: str
    availableQuantity: str
    entryDate: date

class InventoryCreate(InventoryBase):
    pass

class InventoryResponse(InventoryBase):
    id: int

    class Config:
        from_attributes = True
