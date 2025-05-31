"""Schemas for Report data validation and serialization."""

# pylint: disable=too-few-public-methods

from datetime import date
from pydantic import BaseModel, Field


class ReportBase(BaseModel):
    """Base fields for a report."""

    type: str = Field(..., min_length=1, example="Ventas")
    dateReport: date = Field(..., example="2025-05-28")
    content: str = Field(..., min_length=1, example="Informe detallado de ventas del mes.")


class ReportCreate(ReportBase):
    """Schema for creating a report."""
    pass


class ReportResponse(ReportBase):
    """Schema for returning a report with ID."""

    id: int

    class Config:
        orm_mode = True 
        from_attributes = True 


class TopSpenderResponse(BaseModel):
    """Schema for top-spending client name."""
    
    name: str = Field(..., example="Juan Pérez")
