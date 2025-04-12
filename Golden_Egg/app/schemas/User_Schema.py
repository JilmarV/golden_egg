from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    phoneNumber: str
    email: str
    userName: str
    password: str
    address: str
    enabled: bool

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True