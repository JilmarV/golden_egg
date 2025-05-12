from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db   
from app.Order.Order_Schema import *
from app.Order.Order_Repository import *

def read_orders_serv(db: Session):
    return read_orders(db)

def read_order_serv(order_id: int, db: Session = Depends(get_db)):
    return read_order(order_id, db)

def create_order_serv(order: OrderCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

def update_order_serv(order_id: int, order_update: OrderCreate, db: Session = Depends(get_db)):
    existing_order = read_order(order_id, db)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    user = db.query(User).filter(User.id == order_update.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return update_order(order_id, order_update, db)

def delete_order_serv(order_id: int, db: Session = Depends(get_db)):
    return delete_order(order_id, db)