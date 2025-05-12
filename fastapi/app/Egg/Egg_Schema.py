from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.Bill.Bill_Schema import *
from fastapi.app.Supplier.supplier_repository import *

# Base schema for Egg, defining common attributes
class EggBase(BaseModel):
    nameProduct: str
    avalibleQuantity: int
    entryDate: date
    expirationDate: date
    sellprice: float
    entryprice: float
    color: str  # Color of the egg
    category: str  # Category of the egg (e.g., organic, free-range)
    supplier_id: int  # ID of the supplier
    inventory_id: int  # ID of the inventory
    type_egg_id: int
        
# Schema for creating a new Egg, inheriting from EggBase
class EggCreate(EggBase):
    pass

# Response schema for Egg, including additional attributes for response purposes
class EggResponse(EggBase):
    id: int  # Unique identifier for the egg
    supplier: Optional[SupplierResponse] = None  # Supplier details (optional)
    #inventory: Optional[InventoryResponse] = None  # Inventory details (optional)

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with ORMs like SQLAlchemy