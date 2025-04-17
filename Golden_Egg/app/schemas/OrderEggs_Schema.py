from pydantic import BaseModel
from typing import Optional

class OrderEggsBase(BaseModel):
    order_id: int
    egg_id: int

    class Config:
        from_attributes = True


class OrderEggsCreate(OrderEggsBase):
    pass


class OrderEggsUpdate(BaseModel):
    order_id: Optional[int] = None
    egg_id: Optional[int] = None

    class Config:
        from_attributes = True


class OrderEggs(OrderEggsBase):
    id: int
    order_rel: Optional["Order"] = None
    egg_rel: Optional["Egg"] = None

    class Config:
        from_attributes = True