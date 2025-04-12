from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    phoneNumber: str
    email: str
    address: str
    enabled: bool

class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int
    class Config:
        orm_mode = True