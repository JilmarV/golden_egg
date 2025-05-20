"""Schema module for Order models."""

# pylint: disable=too-few-public-methods

from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.User.user_schema import UserResponse


class OrderBase(BaseModel):
    """Base schema for Order."""

    totalPrice: float
    state: str
    user_id: int


class OrderCreate(OrderBase):
    """Schema for creating a new Order."""


class OrderResponse(OrderBase):
    """Schema for Order response."""

    id: int
    orderDate: datetime
    totalPrice: float
    state: str
    user: Optional[UserResponse] = None

    class Config:
        """Configuration for Pydantic model."""

        from_attributes = True
