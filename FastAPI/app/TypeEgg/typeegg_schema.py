"""Pydantic schemas for the TypeEgg model."""

from pydantic import BaseModel


class TypeEggBase(BaseModel):
    """Base schema for TypeEgg with common attributes."""

    name: str


class TypeEggCreate(TypeEggBase):
    """Schema for creating a new TypeEgg."""


class TypeEggResponse(TypeEggBase):
    """Schema for returning TypeEgg data."""

    id: int

    class Config:
        """Pydantic configuration to enable ORM mode."""

        from_attributes = True
