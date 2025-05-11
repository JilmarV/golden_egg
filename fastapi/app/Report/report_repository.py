"""Repository functions for managing report data in the database."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.Report.report_model import Report
from app.Report.report_schema import ReportCreate
from fastapi import Depends, HTTPException


def create_report(report: ReportCreate, db: Session):
    """Creates a new report."""
    db_report = Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def read_reports(db: Session = Depends(get_db)):
    """Retrieves all reports."""
    return db.query(Report).all()


def read_report(report_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific report by ID."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


def delete_report(report_id: int, db: Session = Depends(get_db)):
    """Deletes a report by ID."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}


def update_report(report_id: int, report_update: ReportCreate, db: Session = Depends(get_db)):
    """Updates a report by ID."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in report_update.dict(exclude_unset=True).items():
        setattr(report, key, value)

    db.commit()
    db.refresh(report)
    return report
