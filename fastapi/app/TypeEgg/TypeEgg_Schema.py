from pydantic import BaseModel

class TypeEggBase(BaseModel):
    name: str

class TypeEggCreate(TypeEggBase):
    pass

class TypeEggResponse(TypeEggBase):
    id: int

    class Config:
        from_attributes = True
