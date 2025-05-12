"""Schema module for Pay models."""

# pylint: disable=too-few-public-methods

from typing import Optional
from pydantic import BaseModel

from fastapi.app.User.user_schema import UserResponse
from fastapi.app.Bill.Bill_Schema import BillResponse


class PayBase(BaseModel):
    """Shared properties of a payment."""
    amountPaid: float
    paymentMethod: str
    user_id: int
    bill_id: int


class PayCreate(PayBase):
    """Input schema for creating a new payment."""
    # No additional fields required; inherits from PayBase.


class PayResponse(PayBase):
    """Output schema for returning payment data, including related user and bill."""
    id: int
    user: Optional[UserResponse] = None
    bill: Optional[BillResponse] = None

    class Config:
        """Pydantic configuration for ORM mode."""
        orm_mode = True
