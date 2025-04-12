from sqlalchemy.orm import Session
from models.Report import Report
from schemas.Report_Schema import ReportCreate


def create_Report(db: Session, report: ReportCreate):
    db_Report = Report(**report.dict())
    db.add(db_Report)
    db.commit()
    db.refresh(db_Report)
    return db_Report

def get_Report(db: Session, report_id: int):
    return db.query(Report).filter(Report.id == report_id).first()