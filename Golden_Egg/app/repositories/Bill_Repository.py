from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.Bill import Bill
from app.schemas.Bill_Schema import BillCreate, BillUpdate

class BillRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_bill(self, bill_id: int) -> Optional[Bill]:
        return self.db.query(Bill).filter(Bill.id == bill_id).first()

    def get_bills(self, skip: int = 0, limit: int = 100) -> List[Bill]:
        return self.db.query(Bill).offset(skip).limit(limit).all()

    def get_bills_by_order(self, order_id: int) -> Optional[Bill]:
        return self.db.query(Bill).filter(Bill.order_id == order_id).first()

    def create_bill(self, bill: BillCreate) -> Bill:
        db_bill = Bill(**bill.model_dump())
        self.db.add(db_bill)
        self.db.commit()
        self.db.refresh(db_bill)
        return db_bill

    def update_bill(self, bill_id: int, bill: BillUpdate) -> Optional[Bill]:
        db_bill = self.get_bill(bill_id)
        if db_bill:
            update_data = bill.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_bill, field, value)
            self.db.commit()
            self.db.refresh(db_bill)
        return db_bill

    def delete_bill(self, bill_id: int) -> bool:
        db_bill = self.get_bill(bill_id)
        if db_bill:
            self.db.delete(db_bill)
            self.db.commit()
            return True
        return False