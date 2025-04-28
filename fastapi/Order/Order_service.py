from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db   
from fastapi.Order.Order_schema import OrderCreate
from fastapi.Order.Order_repository import read_order, read_orders, delete_order, create_order, update_order

def read_orders_serv(db: Session):
    return read_orders(db)

def read_order_serv(order_id: int, db: Session = Depends(get_db)):
    return read_order(order_id, db)

def create_order_serv(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(order, db)

def delete_order_serv(order_id: int, db: Session = Depends(get_db)):
    return delete_order(order_id, db)

def update_order_serv(order_id: int, order_update: OrderCreate, db: Session = Depends(get_db)):
    return update_order(order_id, order_update, db)