from sqlalchemy.orm import Session
from repositories.Pay_Repository import create_Pay, get_Pay
from schemas.Pay_Schema import PayCreate


def create_new_pay(db: Session, pay: PayCreate):
    return create_Pay(db, pay)


def fetch_pay(db: Session, pay_id: int):
    return get_Pay(db, pay_id)