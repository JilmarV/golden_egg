"""Service layer for handling Report operations."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.Report.report_schema import ReportCreate
from app.Report.report_repository import (
    read_reports,
    read_report,
    create_report,
    delete_report,
    update_report,
)
from fastapi import Depends


def read_reports_serv(db: Session = Depends(get_db)):
    """Retrieves all reports."""
    return read_reports(db)


def read_report_serv(report_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific report by ID."""
    return read_report(report_id, db)


def create_report_serv(report: ReportCreate, db: Session = Depends(get_db)):
    """Creates a new report."""
    return create_report(report, db)


def delete_report_serv(report_id: int, db: Session = Depends(get_db)):
    """Deletes a report by ID."""
    return delete_report(report_id, db)


def update_report_serv(report_id: int, report_update: ReportCreate, db: Session = Depends(get_db)):
    """Updates an existing report."""
    return update_report(report_id, report_update, db)
