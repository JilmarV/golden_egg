from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import Depends, HTTPException
from app.OrderEgg.OrderEgg_Schema import *
from app.OrderEgg.OrderEgg_Model import *

def create_orderEgg(orderEgg: OrderEggCreate, db: Session):
    db_OrderEgg = OrderEgg(**orderEgg.dict())
    db.add(db_OrderEgg)
    db.commit()
    db.refresh(db_OrderEgg)
    return db_OrderEgg

def read_orderEggs(db: Session = Depends(get_db)):
    orderEggs = db.query(OrderEgg).all()
    return orderEggs

def read_orderEgg(orderEgg_id: int, db: Session = Depends(get_db)):
    orderEgg = db.query(OrderEgg).filter(OrderEgg.id == orderEgg_id).first()
    if orderEgg is None:
        raise HTTPException(status_code=404, detail="OrderEgg not found")
    return orderEgg

def delete_orderEgg(orderEgg_id: int, db: Session = Depends(get_db)):
    orderEgg = db.query(OrderEgg).filter(OrderEgg.id == orderEgg_id).first()
    if orderEgg is None:
        raise HTTPException(status_code=404, detail="OrderEgg not found")
    db.delete(orderEgg)
    db.commit()
    return {"message": "OrderEgg deleted successfully"}

def update_orderEgg(orderEgg_id: int, orderEgg_update: OrderEggCreate, db: Session = Depends(get_db)):
    orderEgg = db.query(OrderEgg).filter(OrderEgg.id == orderEgg_id).first()
    if orderEgg is None:
        raise HTTPException(status_code=404, detail="OrderEgg not found")
    
    for key, value in orderEgg_update.dict(exclude_unset=True).items():
        setattr(orderEgg, key, value)
    
    db.commit()
    db.refresh(orderEgg)
    return orderEgg