"""Service module for Pay operations."""

# pylint: disable=no-name-in-module
  
from sqlalchemy.orm import Session

from fastapi import Depends
from app.db.session import get_db  
from app.Pay.pay_schema import PayCreate
from app.Pay.pay_repository import (
    create_pay,
    read_pays,
    read_pay,
    update_pay,
    delete_pay,
    total_earnings,
    total_earnings_by_month
)

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

def get_total_earnings_serv(db: Session = Depends(get_db)):
    return total_earnings(db)

def get_total_earnings_by_month_serv(year: int, month: int, db: Session = Depends(get_db)) -> float:
    return total_earnings_by_month(db, year, month)