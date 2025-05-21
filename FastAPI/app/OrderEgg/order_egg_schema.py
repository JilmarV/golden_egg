"""Schema module for OrderEgg models."""

# pylint: disable=too-few-public-methods

from pydantic import BaseModel
from app.Egg.egg_schema import EggResponse
from app.Order.order_schema import OrderResponse
from typing import Optional

class OrderEggBase(BaseModel):
    """Base schema for OrderEgg."""

    quantity: int
    unit_price: float
    sub_total: float
    egg_id: int
    order_id: int


class OrderEggCreate(OrderEggBase):
    """Schema for creating a new OrderEgg."""


class OrderEggResponse(OrderEggBase):
    """Schema for OrderEgg response."""
    id: int
    quantity: int
    unit_price: float
    sub_total: float
    class Config:
        """Configuration for Pydantic model."""

        from_attributes = True

        
