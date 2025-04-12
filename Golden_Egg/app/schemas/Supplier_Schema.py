from pydantic import BaseModel

class SupplierBase(BaseModel):
    name: str
    addres: str

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    class Config:
        orm_mode = True