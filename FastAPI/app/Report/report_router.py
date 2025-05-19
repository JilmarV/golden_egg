"""Router for handling report-related API endpoints."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.db.session import get_db
from app.Report.report_schema import (
    ReportCreate,
    ReportResponse,
    TopSpenderResponse,
)
from app.Bill.bill_schema import BillResponse
from app.Report.report_service import (
    create_report_serv,
    read_report_serv,
    delete_report_serv,
    read_reports_serv,
    update_report_serv,
    get_staff_bills_serv,
    get_client_bills_serv,
    get_monthly_total_client_bills_serv,
    get_top_client_this_month_serv,
)

router = APIRouter()


@router.post("/", status_code=201, response_model=ReportResponse)
def create_report_route(report: ReportCreate, db: Session = Depends(get_db)):
    """Creates a new report."""
    return create_report_serv(report, db)


@router.get("/{report_id}", response_model=ReportResponse)
def get_report_route(report_id: int, db: Session = Depends(get_db)):
    """Retrieves a report by ID."""
    return read_report_serv(report_id, db)


@router.delete("/{report_id}")
def delete_report_route(report_id: int, db: Session = Depends(get_db)):
    """Deletes a report by ID."""
    return delete_report_serv(report_id, db)


@router.get("/", response_model=list[ReportResponse])
def read_reports_route(db: Session = Depends(get_db)):
    """Retrieves all reports."""
    return read_reports_serv(db)


@router.put("/{report_id}", response_model=ReportResponse)
def update_report_route(
    report_id: int, report_update: ReportCreate, db: Session = Depends(get_db)
):
    """Updates a report by ID."""
    return update_report_serv(report_id, report_update, db)


@router.get("/bills/staff", response_model=list[BillResponse])
def get_bills_staff_route(db: Session = Depends(get_db)):
    """Returns bills where user is Admin or Employee."""
    return get_staff_bills_serv(db)


@router.get("/bills/clients", response_model=list[BillResponse])
def get_bills_client_route(db: Session = Depends(get_db)):
    """Returns bills where user is Client."""
    return get_client_bills_serv(db)


@router.get("/bills/clients/month-total", response_model=float)
def get_total_client_bills_route(db: Session = Depends(get_db)):
    """Returns total price of client bills this month."""
    return get_monthly_total_client_bills_serv(db)


@router.get("/bills/clients/top-spender", response_model=TopSpenderResponse)
def get_top_spender_route(db: Session = Depends(get_db)):
    """Returns the name of the client who spent the most this month."""
    return {"name": get_top_client_this_month_serv(db)}
