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

    availableQuantity: int
    expirationDate: date
    entryDate: date
    sellPrice: float
    entryPrice: float
    color: str
    type_egg_id: int
    supplier_id: int 


class EggCreate(EggBase):
    """Input schema for creating a new egg."""


class EggResponse(EggBase):
    """Output schema for returning egg data, including related supplier."""

    id: int
    supplier: Optional[SupplierResponse] = None
    type_egg: Optional[TypeEggResponse] = None

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True


class EggSummaryDto(BaseModel):
    """Egg model, grouping by type and color."""

    type_egg: TypeEggResponse
    color: str
    sellPrice: float
    expirationDate: date

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True
