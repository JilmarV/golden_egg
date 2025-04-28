from pydantic import BaseModel
from typing import Optional
#from User.User_Schema import UserResponse
#from Bill.Bill_Schema import BillResponse

class PayBase(BaseModel):
    amountPaid: float
    paymentMethod: str
    user_id: int
    bill_id: int

class PayCreate(PayBase):
    pass

class PayResponse(PayBase):
    id: int
    #user: Optional[UserResponse] = None
    #bill: Optional[BillResponse] = None

    class Config:
        from_attributes = True