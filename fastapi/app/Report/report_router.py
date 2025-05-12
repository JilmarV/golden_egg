"""Router for handling report-related API endpoints."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.Report.report_schema import ReportCreate, ReportResponse
from app.Report.report_service import (
    create_report_serv,
    read_report_serv,
    delete_report_serv,
    read_reports_serv,
    update_report_serv,
)
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/report/", status_code=201, response_model=ReportResponse)
def create_report_route(report: ReportCreate, db: Session = Depends(get_db)):
    """Creates a new report."""
    return create_report_serv(report, db)


@router.get("/report/{report_id}", response_model=ReportResponse)
def get_report_route(report_id: int, db: Session = Depends(get_db)):
    """Retrieves a report by ID."""
    return read_report_serv(report_id, db)


@router.delete("/report/{report_id}")
def delete_report_route(report_id: int, db: Session = Depends(get_db)):
    """Deletes a report by ID."""
    return delete_report_serv(report_id, db)


@router.get("/report/", response_model=list[ReportResponse])
def read_reports_route(db: Session = Depends(get_db)):
    """Retrieves all reports."""
    return read_reports_serv(db)


@router.put("/report/{report_id}", response_model=ReportResponse)
def update_report_route(report_id: int, report_update: ReportCreate, db: Session = Depends(get_db)):
    """Updates a report by ID."""
    return update_report_serv(report_id, report_update, db)
