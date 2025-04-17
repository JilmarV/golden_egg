from pydantic import BaseModel
from typing import Optional, List


class SupplierBase(BaseModel):
    name: str
    address: str

    class Config:
        from_attributes = True


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True


class Supplier(SupplierBase):
    id: int
    inventory_items: List["Inventory"] = []

    class Config:
        from_attributes = True