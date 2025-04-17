from pydantic import BaseModel
from typing import Optional

class UserRoleBase(BaseModel):
    user_id: int
    role_id: int

    class Config:
        from_attributes = True

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleUpdate(BaseModel):
    user_id: Optional[int] = None
    role_id: Optional[int] = None

    class Config:
        from_attributes = True

class UserRole(UserRoleBase):
    id: int
    user: Optional["User"] = None
    role: Optional["Role"] = None

    class Config:
        from_attributes = True