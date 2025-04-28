from pydantic import BaseModel
from datetime import date
from typing import Optional
from Bill.Bill_Schema import *
from Inventory.Inventory_Repository import *
from Supplier.Supplier_Repository import *

# Base schema for Egg, defining common attributes
class EggBase(BaseModel):
    type_egg: str  # Type of egg (e.g., chicken, duck)
    color = str  # Color of the egg
    expirationDate: date  # Expiration date of the egg
    category: str  # Category of the egg (e.g., organic, free-range)
    supplier_id: int  # ID of the supplier
    inventory_id: int  # ID of the inventory
    
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