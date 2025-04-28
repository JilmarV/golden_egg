from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    username: str
    address: str
    enabled: bool

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True