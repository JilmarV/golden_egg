"""Service module for Bill operations."""

# pylint: disable=no-name-in-module

from datetime import datetime
from calendar import monthrange
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.Order.order_model import Order
from app.Bill.bill_model import Bill
from app.Bill.bill_repository import (
    create_bill,
    delete_bill,
    get_all_bills_for_company,
    get_all_bills_for_customers,
    get_best_customer_of_month,
    get_bill_by_id,
    update_bill,
    count_customer_bills_in_range,
    get_monthly_sales_total,
)
from app.Bill.bill_schema import BillCreate


def read_bills_serv(db: Session):
    """Retrieve all bills from the database."""
    return db.query(Bill).all()


def read_bill_serv(bill_id: int, db: Session):
    """Retrieve a single bill by ID, or raise 404 if not found."""
    bill = get_bill_by_id(bill_id, db)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


def create_bill_serv(bill: BillCreate, db: Session):
    """Create a new bill after validating the input."""
    order = db.query(Order).filter(Order.id == bill.order_id).first()
    validate_bill_or_throw(order, bill.totalprice, bill.issueDate)
    return create_bill(bill, db)


def delete_bill_serv(bill_id: int, db: Session):
    """Delete a bill by ID, or raise 404 if not found."""
    bill = get_bill_by_id(bill_id, db)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return delete_bill(bill_id, db)


def update_bill_serv(bill_id: int, bill_update: BillCreate, db: Session):
    """Update an existing bill after validating the input."""
    bill = get_bill_by_id(bill_id, db)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    order = db.query(Order).filter(Order.id == bill_update.order_id).first()
    validate_bill_or_throw(order, bill_update.totalprice, bill_update.issueDate)
    return update_bill(bill_id, bill_update, db)


def get_bills_by_customer_serv(customer_id: int, db: Session):
    """Retrieve all bills for a specific customer by user ID."""
    bills = (
        db.query(Bill)
        .join(Bill.order)
        .filter(Order.user_id == customer_id)
        .all()
    )
    return bills


def count_customer_bills_current_month_serv(db: Session):
    """Count the number of bills for users with role 'CUSTOMER' issued this month."""
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day = monthrange(now.year, now.month)[1]
    end = now.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
    return count_customer_bills_in_range(start, end, db)


def get_best_customer_of_month_serv(db: Session) -> str:
    """Get the best customer of the month based on number of bills issued."""
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    result = get_best_customer_of_month(start, end, db)
    if not result:
        return None
    return result


def get_all_bills_for_company_serv(db: Session):
    """Retrieve all bills for users with company roles."""
    return get_all_bills_for_company(db)


def get_all_bills_for_customers_serv(db: Session):
    """Retrieve all bills associated with customers."""
    return get_all_bills_for_customers(db)


def get_monthly_sales_total_serv(db: Session) -> float:
    """Retrieve the total amount of sales for the current month."""
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    total = get_monthly_sales_total(start, end, db)
    return total or 0.0


def validate_bill_or_throw(order: Order, totalprice: float, issue_date: datetime):
    """
    Validates a bill's order, total price, and issue date.
    Raises an HTTPException if any validation fails.
    """
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order with the given ID does not exist"
        )

    if totalprice <= 0:
        raise HTTPException(
            status_code=400,
            detail="Total price must be greater than zero"
        )

    if issue_date > datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Issue date cannot be in the future"
        )
