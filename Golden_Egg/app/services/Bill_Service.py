from sqlalchemy.orm import Session
from repositories.Bill_Repository import create_Bill, get_Bill
from schemas.Bill_Schema import BillCreate


def create_new_bill(db: Session, bill: BillCreate):
    return create_Bill(db, bill)


def fetch_bill(db: Session, bill_id: int):
    return get_Bill(db, bill_id)