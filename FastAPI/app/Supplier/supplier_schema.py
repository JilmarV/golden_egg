"""Schemas for supplier creation and response models."""

# pylint: disable=too-few-public-methods

from typing import List, Optional
from pydantic import BaseModel


class SupplierCreate(BaseModel):
    """Schema for creating a new supplier."""
    name: str
    address: str


class SupplierResponse(BaseModel):
    """Schema for responding with supplier data."""
    id: int
    name: str
    address: str

    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True
