from pydantic import BaseModel
from typing import Optional, List

class RoleBase(BaseModel):
    roleName: str

    class Config:
        from_attributes = True


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    roleName: Optional[str] = None

    class Config:
        from_attributes = True


class Role(RoleBase):
    roleId: int
    user_roles: List["UserRole"] = []

    class Config:
        from_attributes = True