from pydantic import BaseModel
from datetime import date
from typing import Optional
from Supplier.Supplier_Schema import SupplierResponse
from Inventory.Inventory_Schema import InventoryResponse
from TypeEgg.TypeEgg_Schema import TypeEggResponse

class EggBase(BaseModel):
    color: str
    buy_price: float
    sale_price: Optional[float] = None
    expiration_date: date
    quantity: int
    type_id: int
    supplier_id: int
    inventory_id: int

class EggCreate(EggBase):
    pass

class EggResponse(EggBase):
    id: int
    type: Optional[TypeEggResponse] = None
    supplier: Optional[SupplierResponse] = None
    inventory: Optional[InventoryResponse] = None

    class Config:
        orm_mode = True
