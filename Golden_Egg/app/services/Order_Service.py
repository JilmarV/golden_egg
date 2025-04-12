from sqlalchemy.orm import Session
from repositories.Order_Repository import create_Order, get_Order
from schemas.Order_Schema import OrderCreate


def create_new_order(db: Session, order: OrderCreate):
    return create_Order(db, order)


def fetch_order(db: Session, order_id: int):
    return get_Order(db, order_id)