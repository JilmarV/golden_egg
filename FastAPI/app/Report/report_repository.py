"""Repository functions for managing report data in the database."""

# pylint: disable=not-callable

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import desc
from app.db.session import get_db
from app.Report.report_model import Report
from app.Report.report_schema import ReportCreate
from app.Bill.bill_model import Bill
from app.Order.order_model import Order
from app.User.user_model import User
from app.Role.role_model import Role


def create_report(report: ReportCreate, db: Session):
    """Creates a new report."""
    db_report = Report(**report.model_dump())
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


def update_report(
    report_id: int, report_update: ReportCreate, db: Session = Depends(get_db)
):
    """Updates a report by ID."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in report_update.model_dump(exclude_unset=True).items():
        setattr(report, key, value)

    db.commit()
    db.refresh(report)
    return report


def get_bills_by_staff_roles(db: Session = Depends(get_db)):
    """Returns all bills where the user in the order has role Employee or Admin."""
    return (
        db.query(Bill)
        .join(Bill.order)
        .join(Order.user)
        .join(User.roles)
        .filter(Role.name.in_(["Employee", "Admin"]))
        .all()
    )


def get_bills_by_client_role(db: Session = Depends(get_db)):
    """Returns all bills where the user in the order has role CUSTOMER."""
    return (
        db.query(Bill)
        .join(Bill.order)
        .join(Order.user)
        .join(User.roles)
        .filter(Role.name == "CUSTOMER")
        .all()
    )


def get_total_client_bills_this_month(db: Session = Depends(get_db)):
    """Returns total price of bills issued to clients this month."""
    start_of_month = datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    total = (
        db.query(func.sum(Bill.totalprice))
        .join(Bill.order)
        .join(Order.user)
        .join(User.roles)
        .filter(Role.name == "CUSTOMER", Bill.issueDate >= start_of_month)
        .scalar()
    )
    return total or 0.0


def get_top_client_spender_this_month(db: Session = Depends(get_db)):
    """Returns the name of the client who has spent the most this month."""
    start_of_month = datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    ).date()
    result = (
        db.query(User.name, func.sum(Bill.totalprice).label("total_spent"))
        .join(User.orders)
        .join(Order.bill)
        .join(User.roles)
        .filter(Role.name == "CUSTOMER", Bill.issueDate >= start_of_month)
        .group_by(User.id)
        .order_by(desc("total_spent"))
        .first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No client bills found this month")
    return result.name
