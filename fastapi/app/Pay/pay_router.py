"""Router module for Pay endpoints."""

# pylint: disable=import-error, no-name-in-module

from typing import List

from sqlalchemy.orm import Session

from app.db.session import get_db
from fastapi.app.Pay.pay_schema import PayCreate, PayResponse
from fastapi.app.Pay.pay_service import (
    create_pay,
    read_pays,
    read_pay,
    update_pay,
    delete_pay,
)
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/pay/", status_code=201, response_model=PayResponse)
def create_pay_route(pay: PayCreate, db: Session = Depends(get_db)):
    """Create a new payment via POST."""
    return create_pay(pay, db)

@router.get("/pay/{pay_id}", response_model=PayResponse)
def get_pay_route(pay_id: int, db: Session = Depends(get_db)):
    """Get a payment by ID via GET."""
    return read_pay(pay_id, db)

@router.get("/pay/", response_model=List[PayResponse])
def read_pays_route(db: Session = Depends(get_db)):
    """Get all payments via GET."""
    return read_pays(db)

@router.put("/pay/{pay_id}", response_model=PayResponse)
def update_pay_route(
    pay_id: int,
    pay_update: PayCreate,
    db: Session = Depends(get_db),
):
    """Update a payment by ID via PUT."""
    return update_pay(pay_id, pay_update, db)

@router.delete("/pay/{pay_id}")
def delete_pay_route(pay_id: int, db: Session = Depends(get_db)):
    """Delete a payment by ID via DELETE."""
    delete_pay(pay_id, db)
    return {"message": "Pay deleted successfully"}
