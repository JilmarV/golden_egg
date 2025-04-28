from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import Depends, HTTPException
from Pay.Pay_Schema import *
from Pay.Pay_Model import *

def create_pay(pay: PayCreate, db: Session):
    db_Pay = Pay(**pay.dict())
    db.add(db_Pay)
    db.commit()
    db.refresh(db_Pay)
    return db_Pay

def read_pays(db: Session = Depends(get_db)):
    pays = db.query(Pay).all()
    return pays

def read_pay(pay_id: int, db: Session = Depends(get_db)):
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if pay is None:
        raise HTTPException(status_code=404, detail="Pay not found")
    return pay

def delete_pay(pay_id: int, db: Session = Depends(get_db)):
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if pay is None:
        raise HTTPException(status_code=404, detail="Pay not found")
    db.delete(pay)
    db.commit()
    return {"message": "Pay deleted successfully"}

def update_pay(pay_id: int, pay_update: PayCreate, db: Session = Depends(get_db)):
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if pay is None:
        raise HTTPException(status_code=404, detail="Pay not found")
    
    for key, value in pay_update.dict(exclude_unset=True).items():
        setattr(pay, key, value)
    
    db.commit()
    db.refresh(pay)
    return pay