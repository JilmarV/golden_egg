from pydantic import BaseModel
from datetime import date

class EggBase(BaseModel):
    color: str
    
class EggCreate(EggBase):
    pass

class EggResponse(EggBase):
    id: int
    class Config:
        orm_mode = True