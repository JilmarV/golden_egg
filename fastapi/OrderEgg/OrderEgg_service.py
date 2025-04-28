from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db   
from fastapi.OrderEgg.OrderEgg_schema import OrderEggCreate
from fastapi.OrderEgg.OrderEgg_repository import read_orderEgg, read_orderEggs, delete_orderEgg, create_orderEgg

def read_orderEggs_serv(db: Session):
    return read_orderEggs(db)

def read_orderEgg_serv(orderEgg_id: int, db: Session = Depends(get_db)):
    return read_orderEgg(orderEgg_id, db)

def create_orderEgg_serv(orderEgg: OrderEggCreate, db: Session = Depends(get_db)):
    return create_orderEgg(orderEgg, db)

def delete_orderEgg_serv(orderEgg_id: int, db: Session = Depends(get_db)):
    return delete_orderEgg(orderEgg_id, db)