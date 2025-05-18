"""Schemas for Report data validation and serialization."""

# pylint: disable=too-few-public-methods

from datetime import date
from pydantic import BaseModel


class ReportBase(BaseModel):
    """Base fields for a report."""

    type: str
    dateReport: date
    content: str


class ReportCreate(ReportBase):
    """Schema for creating a report."""


class ReportResponse(ReportBase):
    """Schema for returning a report with ID."""

    id: int

    class Config:
        """Pydantic configuration for ORM compatibility."""

        from_attributes = True


class TopSpenderResponse(BaseModel):
    """Schema for top-spending client name."""

    name: str
