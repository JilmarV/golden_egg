from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    name: str
    phoneNumber: str
    email: EmailStr
    userName: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
    address: Optional[str] = None
    enabled: Optional[bool] = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phoneNumber: Optional[str] = None
    email: Optional[EmailStr] = None
    userName: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    enabled: Optional[bool] = None

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    address: Optional[str] = None
    enabled: Optional[bool] = True
    roles: List["UserRole"] = []

    class Config:
        from_attributes = True