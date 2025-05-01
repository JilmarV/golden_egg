from pydantic import BaseModel
from datetime import date

class ReportBase(BaseModel):
    type: str
    dateReport: date
    content: str

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int

    class Config:
        from_attributes = True