from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.pay import Pay
from app.schemas.Pay_Schema import PayCreate, PayUpdate

class PayRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_pay(self, pay_id: int) -> Optional[Pay]:
        return self.db.query(Pay).filter(Pay.id == pay_id).first()

    def get_payments_by_bill(self, bill_id: int) -> List[Pay]:
        return self.db.query(Pay).filter(Pay.bill_id == bill_id).all()

    def create_pay(self, pay: PayCreate) -> Pay:
        db_pay = Pay(**pay.model_dump())
        self.db.add(db_pay)
        self.db.commit()
        self.db.refresh(db_pay)
        return db_pay

    def update_pay(self, pay_id: int, pay: PayUpdate) -> Optional[Pay]:
        db_pay = self.get_pay(pay_id)
        if db_pay:
            update_data = pay.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_pay, field, value)
            self.db.commit()
            self.db.refresh(db_pay)
        return db_pay

    def delete_pay(self, pay_id: int) -> bool:
        db_pay = self.get_pay(pay_id)
        if db_pay:
            self.db.delete(db_pay)
            self.db.commit()
            return True
        return False