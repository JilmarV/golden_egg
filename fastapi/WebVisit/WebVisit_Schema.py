from pydantic import BaseModel
from datetime import datetime

class WebVisitResponse(BaseModel):
    id: int
    ip: str
    timestamp: datetime

    class Config:
        orm_mode = True
