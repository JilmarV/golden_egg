"""Service layer for handling Report operations."""

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from datetime import datetime

from app.db.session import get_db
from app.Report.report_schema import ReportCreate
from app.Report.report_repository import (
    read_reports,
    read_report,
    create_report,
    delete_report,
    update_report,
)


def read_reports_serv(db: Session = Depends(get_db)):
    """Retrieves all reports."""
    return read_reports(db)


def read_report_serv(report_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific report by ID."""
    return read_report(report_id, db)


def create_report_serv(report: ReportCreate, db: Session = Depends(get_db)):
    """Creates a new report."""
    validate_report_or_throw(report)
    return create_report(report, db)


def update_report_serv(report_id: int, report_update: ReportCreate, db: Session = Depends(get_db)):
    """Updates an existing report."""
    validate_report_or_throw(report_update)
    return update_report(report_id, report_update, db)


def delete_report_serv(report_id: int, db: Session = Depends(get_db)):
    """Deletes a report by ID."""
    return delete_report(report_id, db)


def validate_report_or_throw(report: ReportCreate):
    """Validates the fields of a report and raises exceptions if invalid."""
    if not report.type.strip():
        raise HTTPException(status_code=400, detail="Tipo de reporte no válido")
    if report.dateReport > datetime.now().date():
        raise HTTPException(status_code=400, detail="Fecha de reporte inválida")
    if not report.content.strip():
        raise HTTPException(status_code=400, detail="Contenido inválido")
