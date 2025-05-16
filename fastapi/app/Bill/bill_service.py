"""Service module for Bill operations."""

# pylint: disable=no-name-in-module


from pytest import Session
from fastapi import Depends, HTTPException
from fastapi.app.Order.order_model import Order
from fastapi.app.Bill.bill_model import Bill
from fastapi.app.Bill.bill_repository import (
    create_bill,
    delete_bill,
    get_bill_by_id,
    get_db,
    update_bill,
)
from fastapi.app.Bill.bill_schema import BillCreate

# Service function to read all bills from the database
def read_bills_serv(db: Session):
    """Retrieve all bills from the database."""
    bills = db.query(Bill).all()
    if not bills:
        raise HTTPException(status_code=404, detail="No bills found")
    return bills


# Service function to read a specific bill by its ID
def read_bill_serv(bill_id: int, db: Session = Depends(get_db)):
    """Retrieve a single bill by ID, or raise 404 if not found."""
    bill = get_bill_by_id(bill_id, db)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


# Service function to create a new bill in the database
def create_bill_serv(bill: BillCreate, db: Session = Depends(get_db)):
    """Create a new bill after validating that the order exists."""
    order = db.query(Order).filter(Order.id == bill.order_id).first()
    if not order:
        raise HTTPException(
            status_code=404, detail="Order with the given ID does not exist"
        )

    return create_bill(bill, db)


# Service function to delete a bill by its ID
def delete_bill_serv(bill_id: int, db: Session = Depends(get_db)):
    """Delete a bill by ID, or raise 404 if not found."""
    bill = get_bill_by_id(bill_id, db)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return delete_bill(bill_id, db)


# Service function to update an existing bill by its ID
def update_bill_serv(
    bill_id: int, bill_update: BillCreate, db: Session = Depends(get_db)
):
    """Update an existing bill after validating that the order exists."""
    bill = get_bill_by_id(bill_id, db)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    order = db.query(Order).filter(Order.id == bill_update.order_id).first()
    if not order:
        raise HTTPException(
            status_code=404, detail="Order with the given ID does not exist"
        )

    return update_bill(bill_id, bill_update, db)
