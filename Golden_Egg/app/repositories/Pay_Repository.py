from sqlalchemy.orm import Session
from models.Pay import Pay
from schemas.Pay_Schema import PayCreate


def create_Pay(db: Session, pay: PayCreate):
    db_Pay = Pay(**pay.dict())
    db.add(db_Pay)
    db.commit()
    db.refresh(db_Pay)
    return db_Pay

def get_Pay(db: Session, pay_id: int):
    return db.query(Pay).filter(Pay.id == pay_id).first()