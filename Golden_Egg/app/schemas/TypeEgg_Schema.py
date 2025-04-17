from pydantic import BaseModel
from typing import Optional, List


class TypeEggBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class TypeEggCreate(TypeEggBase):
    pass


class TypeEggUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes = True


class TypeEgg(TypeEggBase):
    id: int
    eggs: List["Egg"] = []

    class Config:
        from_attributes = True