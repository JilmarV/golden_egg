from fastapi import HTTPException
from sqlalchemy.orm import Session
from Pay.Pay_Model import Pay
from Pay.Pay_Schema import PayCreate
from User.User_Model import *
from Bill.Bill_Model import *

def read_pays(db: Session):
    return db.query(Pay).all()

def read_pay(pay_id: int, db: Session):
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if not pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    return pay

def create_pay(pay_data: PayCreate, db: Session):
    user = db.query(User).filter(User.id == pay_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    bill = db.query(Bill).filter(Bill.id == pay_data.bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    new_pay = Pay(
        amountPaid=pay_data.amountPaid,
        paymentMethod=pay_data.paymentMethod,
        user_id=pay_data.user_id,
        bill_id=pay_data.bill_id
    )
    db.add(new_pay)
    db.commit()
    db.refresh(new_pay)
    return new_pay

def delete_pay(pay_id: int, db: Session):
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if not pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(pay)
    db.commit()
    return {"message": "Payment deleted"}

def update_pay(pay_id: int, pay_data: PayCreate, db: Session):
    pay = db.query(Pay).filter(Pay.id == pay_id).first()
    if not pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    user = db.query(User).filter(User.id == pay_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    bill = db.query(Bill).filter(Bill.id == pay_data.bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    pay.amountPaid = pay_data.amountPaid
    pay.paymentMethod = pay_data.paymentMethod
    pay.user_id = pay_data.user_id
    pay.bill_id = pay_data.bill_id

    db.commit()
    db.refresh(pay)
    return pays