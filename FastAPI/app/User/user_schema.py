"""Pydantic schemas for user data handling."""

from pydantic import BaseModel, EmailStr, constr, field_validator
from app.Role.role_schema import RoleResponse
from typing import List
import re


class UserBase(BaseModel):
    """Base schema with common user fields."""

    name: str
    phone_number: constr(min_length=10, max_length=10)
    email: EmailStr
    username: constr(min_length=3, max_length=50)
    address: str
    enabled: bool
    role_ids: List[int]

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value):
        """Validates the phone number format."""
        if not re.fullmatch(r"\+?[0-9\- ]{10,15}", value):
            raise ValueError("Numero de teléfono inválido")
        return value


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str


class UserResponse(BaseModel):
    """Schema for user response data."""

    id: int
    name: str
    phone_number: str
    email: EmailStr
    username: str
    address: str
    enabled: bool
    roles: List[RoleResponse]

    class Config:
        """Pydantic configuration."""

        from_attributes = True
