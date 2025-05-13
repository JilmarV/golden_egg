"""Schema module for Egg models."""

# pylint: disable=too-few-public-methods

from datetime import date
from typing import Optional
from pydantic import BaseModel
from fastapi.app.Supplier.supplier_schema import SupplierResponse


# Base schema for Egg, defining common attributes
class EggBase(BaseModel):
    """Base schema for Egg model."""

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


class EggCreate(EggBase):
    """Input schema for creating a new egg."""

    class Config:
        """Pydantic configuration for ORM mode."""

        orm_mode = True


class EggResponse(EggBase):
    """Output schema for returning egg data, including related supplier."""

    id: int
    supplier: Optional[SupplierResponse] = None
    # inventory: Optional[InventoryResponse] = None

    class Config:
        """Pydantic configuration for ORM mode."""

        orm_mode = True
