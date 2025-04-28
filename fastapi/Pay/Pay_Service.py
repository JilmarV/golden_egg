from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db   
from Pay_Schema import PayCreate
from Pay_Repository import read_pay, read_pays, delete_pay, create_pay, update_pay

def read_pays_serv(db: Session):
    return read_pays(db)

def read_pay_serv(pay_id: int, db: Session = Depends(get_db)):
    return read_pay(pay_id, db)

def create_pay_serv(pay: PayCreate, db: Session = Depends(get_db)):
    return create_pay(pay, db)

def delete_pay_serv(pay_id: int, db: Session = Depends(get_db)):
    return delete_pay(pay_id, db)

def update_pay_serv(pay_id: int, pay_update: PayCreate, db: Session = Depends(get_db)):
    return update_pay(pay_id, pay_update, db)