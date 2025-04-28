from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from Report.Report_Model import *
from Report.Report_Schema import *
from Report.Report_Service import *

router = APIRouter()

@router.post("/report/", status_code=201, response_model=ReportResponse)
def create_report_route(report: ReportCreate, db: Session = Depends(get_db)):
    return create_report_serv(report, db)

@router.get("/report/{report_id}")
def get_report_route(report_id: int, db: Session = Depends(get_db)):
    return read_report_serv(report_id, db)

@router.delete("/report/{report_id}")
def delete_report_route(report_id: int, db: Session = Depends(get_db)):
    return delete_report_serv(report_id, db)

@router.get("/report/")
def read_reports_route(report_id: int, db: Session = Depends(get_db)):
    return read_reports_serv(db)

@router.put("/report/{report_id}")
def update_report_route(report_id: int, report_update: ReportCreate, db: Session = Depends(get_db)):
    return update_report_serv(report_id, report_update, db)