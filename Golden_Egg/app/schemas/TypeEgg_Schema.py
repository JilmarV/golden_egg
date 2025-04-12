from pydantic import BaseModel
from datetime import date

class TypeEggBase(BaseModel):
    name: str

class TypeEggCreate(TypeEggBase):
    pass


class TypeEggResponse(TypeEggBase):
    id: int
    class Config:
        orm_mode = True