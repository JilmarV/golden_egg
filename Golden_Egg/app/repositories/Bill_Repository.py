from sqlalchemy.orm import Session
from models.Bill import Bill
from schemas.Bill_Schema import BillCreate

def create_Bill(db: Session, bill: BillCreate):
    db_Bill = Bill(**bill.dict())
    db.add(db_Bill)
    db.commit()
    db.refresh(db_Bill)
    return db_Bill

def get_Bill(db: Session, bill_id: int):
    return db.query(Bill).filter(Bill.id == bill_id).first()