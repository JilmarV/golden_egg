from pydantic import BaseModel
from typing import Optional
from datetime import date

class ReportBase(BaseModel):
    type: str
    dateReport: date
    content: str

    class Config:
        from_attributes = True

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    type: Optional[str] = None
    dateReport: Optional[date] = None
    content: Optional[str] = None

    class Config:
        from_attributes = True

class Report(ReportBase):
    id: int

    class Config:
        from_attributes = True