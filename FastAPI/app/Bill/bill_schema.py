"""Schema module for Bill models."""

# pylint: disable=too-few-public-methods

from pydantic import BaseModel


# Base schema for a Bill, containing common fields
class BillBase(BaseModel):
    """Shared properties of a bill."""

    totalprice: float  # The total price of the bill
    paid: bool  # Indicates whether the bill has been paid
    order_id: int  # The ID of the associated order


# Schema for creating a new Bill, inherits from BillBase
class BillCreate(BillBase):
    """Input schema for creating a new bill."""

    # No additional fields required; inherits from BillBase.
    class Config:
        """Pydantic configuration for ORM mode."""

        orm_mode = True


# Schema for responding with Bill data, inherits from BillBase
class BillResponse(BillBase):
    """Output schema for returning bill data."""

    id: int  # The unique identifier for the bill

    class Config:
        """Pydantic configuration for ORM mode."""

        orm_mode = True  # Enables compatibility with ORM objects
