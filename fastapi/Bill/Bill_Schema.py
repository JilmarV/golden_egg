from pydantic import BaseModel
from datetime import date

# Base schema for a Bill, containing common fields
class BillBase(BaseModel):
    issueDate: date  # The date the bill was issued
    totalprice: float  # The total price of the bill
    paid: bool  # Indicates whether the bill has been paid
    order_id: int  # The ID of the associated order

# Schema for creating a new Bill, inherits from BillBase
class BillCreate(BillBase):
    pass  # No additional fields, uses the same fields as BillBase

# Schema for responding with Bill data, inherits from BillBase
class BillResponse(BillBase):
    id: int  # The unique identifier for the bill

    class Config:
        orm_mode = True  # Enables compatibility with ORM objects
