from sqlalchemy.orm import Session
from repositories.Report_Repository import create_Report, get_Report
from schemas.Report_Schema import ReportCreate


def create_new_report(db: Session, report: ReportCreate):
    return create_Report(db, report)


def fetch_report(db: Session, report_id: int):
    return get_Report(db, report_id)