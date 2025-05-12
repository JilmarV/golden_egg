"""Pydantic schemas for user data handling."""

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base schema with common user fields."""
    name: str
    phone_number: str
    email: str
    username: str
    address: str
    enabled: bool


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str


class UserResponse(UserBase):
    """Schema for returning user data from the API."""
    id: int

    # pylint: disable=too-few-public-methods
    class Config:
        """Pydantic config to allow ORM integration."""
        from_attributes = True
