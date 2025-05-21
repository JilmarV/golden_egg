"""Service module for Pay operations."""

# pylint: disable=no-name-in-module

from sqlalchemy.orm import Session

from fastapi import Depends
from fastapi import HTTPException
from app.db.session import get_db
from app.Pay.pay_schema import PayCreate
from app.User.user_model import User
from app.Bill.bill_model import Bill
from app.Pay.pay_repository import (
    create_pay,
    read_pays,
    read_pay,
    update_pay,
    delete_pay,
    total_earnings,
    total_earnings_by_month,
)


def read_pays_serv(db: Session):
    """Retrieve all payments from the database."""
    return read_pays(db)


def read_pay_serv(pay_id: int, db: Session = Depends(get_db)):
    """Retrieve a single payment by ID, or raise 404 if not found."""
    return read_pay(pay_id, db)


def create_pay_serv(pay: PayCreate, db: Session = Depends(get_db)):
    """Create a new payment after validating that user and pay exist."""
    if pay.amount_paid <= 0:
        raise HTTPException(
            status_code=400, detail="the amount paid must be greater than 0"
        )
    if not pay.payment_method.strip():
        raise HTTPException(status_code=400, detail="payment method is required")
    user = db.query(User).filter(User.id == pay.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    bill = db.query(Bill).filter(Bill.id == pay.bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return create_pay(pay, db)


def delete_pay_serv(pay_id: int, db: Session = Depends(get_db)):
    """Delete a payment by ID, or raise 404 if not found."""
    return delete_pay(pay_id, db)


def update_pay_serv(pay_id: int, pay_update: PayCreate, db: Session = Depends(get_db)):
    """Update an existing payment after validating that user and pay exist."""
    if pay_update.amount_paid <= 0:
        raise HTTPException(
            status_code=400, detail="the amount paid must be greater than 0"
        )
    if not pay_update.payment_method.strip():
        raise HTTPException(status_code=400, detail="payment method is required")
    user = db.query(User).filter(User.id == pay_update.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    bill = db.query(Bill).filter(Bill.id == pay_update.bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return update_pay(pay_id, pay_update, db)


def get_total_earnings_serv(db: Session = Depends(get_db)):
    """Get total earnings from all payments."""
    return total_earnings(db)


def get_total_earnings_by_month_serv(
    year: int, month: int, db: Session = Depends(get_db)
):
    """Get total earnings for a specific month and year."""
    return total_earnings_by_month(db, year, month)
