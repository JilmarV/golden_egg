"""Router module for Pay endpoints."""

from typing import List

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.Pay.pay_schema import PayCreate, PayResponse
from app.Pay.pay_service import (
    create_pay_serv,
    read_pays_serv,
    read_pay_serv,
    update_pay_serv,
    delete_pay_serv,
    get_total_earnings_serv,
    get_total_earnings_by_month_serv,
)
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/", status_code=201, response_model=PayResponse)
def create_pay_route(pay: PayCreate, db: Session = Depends(get_db)):
    """Create a new payment via POST."""
    return create_pay_serv(pay, db)


@router.get("/{pay_id}", response_model=PayResponse)
def get_pay_route(pay_id: int, db: Session = Depends(get_db)):
    """Get a payment by ID via GET."""
    return read_pay_serv(pay_id, db)


@router.get("/", response_model=List[PayResponse])
def read_pays_route(db: Session = Depends(get_db)):
    """Get all payments via GET."""
    return read_pays_serv(db)


@router.put("/{pay_id}", response_model=PayResponse)
def update_pay_route(
    pay_id: int,
    pay_update: PayCreate,
    db: Session = Depends(get_db),
):
    """Update a payment by ID via PUT."""
    return update_pay_serv(pay_id, pay_update, db)


@router.delete("/{pay_id}")
def delete_pay_route(pay_id: int, db: Session = Depends(get_db)):
    """Delete a payment by ID via DELETE."""
    delete_pay_serv(pay_id, db)
    return {"message": "Pay deleted successfully"}


@router.get("/earnings/total_earnings")
def total_pay_route(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve the total earnings.

    Args:
        db (Session, optional): SQLAlchemy database session dependency.
        Defaults to Depends(get_db).

    Returns:
        The total earnings as calculated by the get_total_earnings_serv service function.
    """
    return get_total_earnings_serv(db)

@router.get("/earnings/total_earnings_month")
def total_pay_month_route(year: int, month: int, db: Session = Depends(get_db)):
    """
    Calculates and returns the total amount paid for a specific month and year.

    Args:
        year (int): The year for which the total payment is to be calculated.
        month (int): The month for which the total payment is to be calculated.
        db (Session, optional): Database session dependency.

    Returns:
        dict: A dictionary containing the total amount paid,
        the specified year, and the specified month.
    """
    total = get_total_earnings_by_month_serv(year, month, db)
    return {"Total Pagado": total, "En el año:": year, "Del mes:": month}
