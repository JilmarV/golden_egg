from pydantic import BaseModel
from typing import Optional

class PayBase(BaseModel):
    amountPaid: float
    paymentMethod: str

    class Config:
        from_attributes = True

class PayCreate(PayBase):
    bill_id: int

class PayUpdate(BaseModel):
    amountPaid: Optional[float] = None
    paymentMethod: Optional[str] = None
    bill_id: Optional[int] = None

    class Config:
        from_attributes = True

class Pay(PayBase):
    id: int
    bill_id: int
    bill: Optional["Bill"] = None

    class Config:
        from_attributes = True