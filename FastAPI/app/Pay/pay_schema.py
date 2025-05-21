"""Schema module for Pay models."""

# pylint: disable=too-few-public-methods

from typing import Optional
from pydantic import BaseModel

from app.User.user_schema import UserResponse


class PayBase(BaseModel):
    """Shared properties of a payment."""

    amount_paid: float
    payment_method: str
    user_id: int
    bill_id: int


class PayCreate(PayBase):
    """Input schema for creating a new payment."""

    # No additional fields required; inherits from PayBase.


class PayResponse(PayBase):
    """Output schema for returning payment data, including related user and bill."""

    id: int
    amount_paid: float
    payment_method: str
    bill_id: int
    user: Optional[UserResponse] = None

    class Config:
        """Pydantic configuration for ORM mode."""

        from_attributes = True
