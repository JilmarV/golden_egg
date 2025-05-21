"""Repository module for Pay operations."""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import HTTPException
from app.Pay.pay_model import Pay
from app.Pay.pay_schema import PayCreate
from app.User.user_model import User


def read_pays(db: Session):
    """Retrieve all payments from the database."""
    return db.query(Pay).all()


def read_pay(pay_id: int, db: Session):
    """Retrieve a single payment by ID, or raise 404 if not found."""
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if not pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    return pay


def create_pay(pay: PayCreate, db: Session):
    """Create a new payment after validating that user and pay exist."""
    user = db.query(User).filter(User.id == pay.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_pay = Pay(**pay.model_dump())
    db.add(db_pay)
    db.commit()
    db.refresh(db_pay)
    return db_pay


def delete_pay(pay_id: int, db: Session):
    """Delete a payment by ID, or raise 404 if not found."""
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if not pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(pay)
    db.commit()
    return {"message": "Payment deleted"}


def update_pay(pay_id: int, pay: PayCreate, db: Session):
    """Update an existing payment after validating that user and pay exist."""
    db_pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if not db_pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    user = db.query(User).filter(User.id == pay.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if not db_pay:
        raise HTTPException(status_code=404, detail="Pay not found")

    for key, value in pay.model_dump().items():
        setattr(db_pay, key, value)
    db.commit()
    db.refresh(db_pay)
    return db_pay


def total_earnings_by_month(db: Session, year: int, month: int) -> float:
    """Calculate the total earnings for a specific month and year."""
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    total = (
        db.query(func.sum(Pay.amount_paid))
        .filter(and_(Pay.issueDate >= start_date, Pay.issueDate < end_date))
        .scalar()
    )
    return total or 0.0


def total_earnings(db: Session):
    """Retrieve all payments from the database."""
    total = db.query(func.sum(Pay.amount_paid)).scalar()  # pylint: disable=not-callable
    return total or 0.0
