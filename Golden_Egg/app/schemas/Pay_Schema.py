from pydantic import BaseModel

class PayBase(BaseModel):
    paymetMethod: str
    amountPaid: float

class PayCreate(PayBase):
    pass


class PayResponse(PayBase):
    id: int
    class Config:
        orm_mode = True