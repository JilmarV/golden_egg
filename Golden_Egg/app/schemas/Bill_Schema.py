from pydantic import BaseModel
from datetime import date

class BillBase(BaseModel):
    issueDate: date
    totalPrice: float
    paid: bool

class BillCreate(BillBase):
    pass


class BillResponse(BillBase):
    id: int
    class Config:
        orm_mode = True