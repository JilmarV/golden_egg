from pydantic import BaseModel

class UserRoleBase(BaseModel):
    user_id: int
    role_id: int

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleResponse(UserRoleBase):
    id: int
    user_id: int
    role_id: int

    class Config:
        orm_mode = True
