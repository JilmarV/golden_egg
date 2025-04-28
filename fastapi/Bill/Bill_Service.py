from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from db.session import get_db
from Bill.Bill_Repository import *
from Bill.Bill_Schema import *

# Service function to read all bills from the database
def read_bills_serv(db: Session):
    return get_all_bills(db)

# Service function to read a specific bill by its ID
def read_bill_serv(bill_id: int, db: Session = Depends(get_db)):
    bill = get_bill_by_id(bill_id, db)

# Service function to create a new bill in the database
def create_bill_serv(bill: BillCreate, db: Session = Depends(get_db)):
    return create_bill(bill, db)

# Service function to delete a bill by its ID
def delete_bill_serv(bill_id: int, db: Session = Depends(get_db)):
    return delete_bill(bill_id, db)

# Service function to update an existing bill by its ID
def update_bill_serv(bill_id: int, bill_update: BillCreate, db: Session = Depends(get_db)):
    return update_bill(bill_id, bill_update, db)
