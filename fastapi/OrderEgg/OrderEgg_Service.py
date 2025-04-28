from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db   
from OrderEgg.OrderEgg_Schema import *
from OrderEgg.OrderEgg_Repository import *

def read_orderEggs_serv(db: Session):
    return read_orderEggs(db)

def read_orderEgg_serv(orderEgg_id: int, db: Session = Depends(get_db)):
    return read_orderEgg(orderEgg_id, db)

def create_orderEgg_serv(orderEgg: OrderEggCreate, db: Session = Depends(get_db)):
    return create_orderEgg(orderEgg, db)

def delete_orderEgg_serv(orderEgg_id: int, db: Session = Depends(get_db)):
    return delete_orderEgg(orderEgg_id, db)