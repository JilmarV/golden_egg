"""Schema module for OrderEgg models."""

# pylint: disable=too-few-public-methods

from pydantic import BaseModel


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

    class Config:
        """Configuration for Pydantic model."""

        from_attributes = True
