from sqlalchemy.orm import Session
from models.Order import Order
from schemas.Order_Schema import OrderCreate


def create_Order(db: Session, order: OrderCreate):
    db_Order = Order(**order.dict())
    db.add(db_Order)
    db.commit()
    db.refresh(db_Order)
    return db_Order

def get_Order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()