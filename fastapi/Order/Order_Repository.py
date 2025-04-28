from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import Depends, HTTPException
from Order.Order_Schema import *
from Order.Order_Model import *

def create_order(order: OrderCreate, db: Session):
    db_Order = Order(**order.dict())
    db.add(db_Order)
    db.commit()
    db.refresh(db_Order)
    return db_Order

def read_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

def update_order(order_id: int, order_update: OrderCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)
    
    db.commit()
    db.refresh(order)
    return order