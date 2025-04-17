from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.Order import Order
from app.schemas.Order_Schema import OrderCreate, OrderUpdate

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_order(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        return self.db.query(Order).offset(skip).limit(limit).all()

    def create_order(self, order: OrderCreate) -> Order:
        db_order = Order(
            totalPrice=order.totalPrice,
            orderDate=order.orderDate,
            state=order.state
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def update_order(self, order_id: int, order: OrderUpdate) -> Optional[Order]:
        db_order = self.get_order(order_id)
        if db_order:
            update_data = order.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_order, field, value)
            self.db.commit()
            self.db.refresh(db_order)
        return db_order

    def delete_order(self, order_id: int) -> bool:
        db_order = self.get_order(order_id)
        if db_order:
            self.db.delete(db_order)
            self.db.commit()
            return True
        return False