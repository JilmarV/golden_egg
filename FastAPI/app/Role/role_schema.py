"""Pydantic schemas for Role entity used in request and response models."""

from pydantic import BaseModel


class RoleBase(BaseModel):
    """Base schema for a Role."""

    name: str


class RoleCreate(RoleBase):
    """Schema for creating a Role."""


class RoleResponse(RoleBase):
    """Schema for returning a Role with ID."""

    id: int

    class Config:
        """Enable ORM mode for response models."""

        from_attributes = True
