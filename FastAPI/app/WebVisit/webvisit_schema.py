"""Pydantic schema for WebVisit responses."""

from datetime import datetime
from pydantic import BaseModel


class WebVisitResponse(BaseModel):
    """Schema for returning web visit information."""

    id: int
    ip: str
    timestamp: datetime

    class Config:
        """Configuration for enabling ORM mode."""

        orm_mode = True
