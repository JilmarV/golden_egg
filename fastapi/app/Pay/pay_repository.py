"""Repository module for Pay operations."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods, wrong-import-order, ungrouped-imports

from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException

from app.db.session import get_db
from fastapi.app.Pay.pay_schema import PayCreate
from fastapi.app.Pay.pay_model import Pay

def create_pay(pay: PayCreate, db: Session):
    """Create a new payment record."""
    db_pay = Pay(**pay.dict())
    db.add(db_pay)
    db.commit()
    db.refresh(db_pay)
    return db_pay

def read_pays(db: Session = Depends(get_db)):
    """Retrieve all payment records."""
    return db.query(Pay).all()

def read_pay(pay_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific payment record by ID."""
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if pay is None:
        raise HTTPException(status_code=404, detail="Pay not found")
    return pay

def delete_pay(pay_id: int, db: Session = Depends(get_db)):
    """Delete a specific payment record by ID."""
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if pay is None:
        raise HTTPException(status_code=404, detail="Pay not found")
    db.delete(pay)
    db.commit()
    return {"message": "Pay deleted successfully"}

def update_pay(pay_id: int, pay_update: PayCreate, db: Session = Depends(get_db)):
    """Update a specific payment record by ID."""
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if pay is None:
        raise HTTPException(status_code=404, detail="Pay not found")

    for key, value in pay_update.dict(exclude_unset=True).items():
        setattr(pay, key, value)

    db.commit()
    db.refresh(pay)
    return pay
