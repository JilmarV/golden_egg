from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import Depends, HTTPException
from Report.Report_Model import *
from Report.Report_Schema import *

def create_report(report: ReportCreate, db: Session):
    db_Report = Report(**report.dict())
    db.add(db_Report)
    db.commit()
    db.refresh(db_Report)
    return db_Report

def read_reports(db: Session = Depends(get_db)):
    reports = db.query(Report).all()
    return reports

def read_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}

def update_report(report_id: int, report_update: ReportCreate, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    for key, value in report_update.dict(exclude_unset=True).items():
        setattr(report, key, value)
    
    db.commit()
    db.refresh(report)
    return report