from pydantic import BaseModel
from typing import Optional
from datetime import date

class InventoryBase(BaseModel):
    nameProduct: str
    entryDate: date
    expirationDate: date
    quantity: int
    supplier_id: int

    class Config:
        from_attributes = True


class InventoryCreate(InventoryBase):
    egg_id: Optional[int] = None


class InventoryUpdate(BaseModel):
    nameProduct: Optional[str] = None
    entryDate: Optional[date] = None
    expirationDate: Optional[date] = None
    quantity: Optional[int] = None
    supplier_id: Optional[int] = None
    egg_id: Optional[int] = None

    class Config:
        from_attributes = True


class Inventory(InventoryBase):
    id: int
    egg_id: Optional[int] = None
    supplier: Optional["Supplier"] = None
    egg: Optional["Egg"] = None

    class Config:
        from_attributes = True