from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from Bill.Bill_Model import *
from Bill.Bill_Schema import *


# Create a new bill in database
def create_bill(bill: BillCreate, db: Session = Depends(get_db)):
    db_bill = Bill(**bill.dict())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

# Retrieves all bills from the database
def get_all_bills(db: Session = Depends(get_db)):
    bills = db.query(Bill).all()
    return bills

# Retrieves a specific bill garden by its ID
def get_bill_by_id(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill

# Updates a specific bill in the database
def update_bill(bill_id: int, bill: BillCreate, db: Session = Depends(get_db)):
    db_bill = db.query(Bill).filter(Bill.id == bill_id).first()
    
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    for key, value in bill.dict().items():
        setattr(db_bill, key, value)
    db.commit()
    db.refresh(db_bill)
    return db_bill

# Deletes a specific bill from the database
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    db_bill = db.query(Bill).filter(Bill.id == bill_id).first()
    
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    db.delete(db_bill)
    db.commit()
    return {"message": "Bill deleted successfully"}