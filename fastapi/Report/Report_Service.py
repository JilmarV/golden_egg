from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db   
from Report.Report_Schema import *
from Report.Report_Repository import *

def read_reports_serv(db: Session):
    return read_reports(db)

def read_report_serv(report_id: int, db: Session = Depends(get_db)):
    return read_report(report_id, db)

def create_report_serv(report: ReportCreate, db: Session = Depends(get_db)):
    return create_report(report, db)

def delete_report_serv(report_id: int, db: Session = Depends(get_db)):
    return delete_report(report_id, db)

def update_report_serv(report_id: int, report_update: ReportCreate, db: Session = Depends(get_db)):
    return update_report(report_id, report_update, db)