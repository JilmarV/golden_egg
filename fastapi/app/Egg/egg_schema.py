"""Schema module for Egg models."""

# pylint: disable=too-few-public-methods

from datetime import date
from typing import Optional
from pydantic import BaseModel
from app.Supplier.supplier_schema import SupplierResponse
from app.TypeEgg.typeegg_schema import TypeEggResponse


# Base schema for Egg, defining common attributes
class EggBase(BaseModel):
    """Base schema for Egg model."""

    avalibleQuantity: int
    entryDate: date
    expirationDate: date
    sellprice: float
    entryprice: float
    color: str  # Color of the egg
    category: str  # Category of the egg (e.g., organic, free-range)
    supplier_id: int  # ID of the supplier
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
    type: Optional[TypeEggResponse] = None
    class Config:
        """Pydantic configuration for ORM mode."""

        orm_mode = True
