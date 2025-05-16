"""Repository module for Pay operations."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods, wrong-import-order, ungrouped-imports

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.app.Pay.pay_model import Pay
from fastapi.app.Pay.pay_schema import PayCreate
from fastapi.app.User.user_model import User
from fastapi.app.Bill.bill_model import Bill

def read_pays(db: Session):
    """Retrieve all payments from the database."""
    return db.query(Pay).all()

def read_pay(pay_id: int, db: Session):
    """Retrieve a single payment by ID, or raise 404 if not found."""
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if not pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    return pay


def create_pay(pay_data: PayCreate, db: Session):
    """Create a new payment after validating that user and bill exist."""
    user = db.query(User).filter(User.id == pay_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    bill = db.query(Bill).filter(Bill.id == pay_data.bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    new_pay = Pay(
        amountPaid=pay_data.amountPaid,
        paymentMethod=pay_data.paymentMethod,
        user_id=pay_data.user_id,
        bill_id=pay_data.bill_id
    )
    db.add(new_pay)
    db.commit()
    db.refresh(new_pay)
    return new_pay


def delete_pay(pay_id: int, db: Session):
    """Delete a payment by ID, or raise 404 if not found."""
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if not pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(pay)
    db.commit()
    return {"message": "Payment deleted"}


def update_pay(pay_id: int, pay_data: PayCreate, db: Session):
    """Update an existing payment after validating that user and bill exist."""
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if not pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    user = db.query(User).filter(User.id == pay_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    bill = db.query(Bill).filter(Bill.id == pay_data.bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    pay.amountPaid = pay_data.amountPaid
    pay.paymentMethod = pay_data.paymentMethod
    pay.user_id = pay_data.user_id
    pay.bill_id = pay_data.bill_id

    db.commit()
    db.refresh(pay)
    return pay

def total_earnings_by_month(db: Session, year: int, month:int) -> float:
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    total = db.query(sum(Pay.amount_paid)).filter(and_(Pay.issueDate >= start_date, Pay.issueDate < end_date)).scalar()
    return total or 0.0

def total_earnings(db: Session):
    """Retrieve all payments from the database."""
    total = db.query(func.sum(Pay.amount_paid)).scalar()
    return total or 0.0