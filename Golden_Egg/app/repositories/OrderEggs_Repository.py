from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.OrderEggs import OrderEggs
from app.schemas.OrderEggs_Schema import OrderEggsCreate

class OrderEggsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_order_eggs(self, order_id: int, egg_id: int) -> Optional[OrderEggs]:
        return self.db.query(OrderEggs).filter(
            OrderEggs.order_id == order_id,
            OrderEggs.egg_id == egg_id
        ).first()

    def get_eggs_for_order(self, order_id: int) -> List[OrderEggs]:
        return self.db.query(OrderEggs).filter(
            OrderEggs.order_id == order_id
        ).all()

    def add_egg_to_order(self, order_egg: OrderEggsCreate) -> OrderEggs:
        db_order_egg = OrderEggs(**order_egg.model_dump())
        self.db.add(db_order_egg)
        self.db.commit()
        self.db.refresh(db_order_egg)
        return db_order_egg

    def remove_egg_from_order(self, order_id: int, egg_id: int) -> bool:
        db_order_egg = self.get_order_eggs(order_id, egg_id)
        if db_order_egg:
            self.db.delete(db_order_egg)
            self.db.commit()
            return True
        return False