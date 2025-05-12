from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db   
from app.OrderEgg.OrderEgg_Schema import *
from app.OrderEgg.OrderEgg_Repository import *

def read_orderEggs_serv(db: Session):
    return read_orderEggs(db)

def read_orderEgg_serv(orderEgg_id: int, db: Session = Depends(get_db)):
    return read_orderEgg(orderEgg_id, db)

def create_orderEgg_serv(orderEgg: OrderEggCreate, db: Session = Depends(get_db)):
    return create_orderEgg

def update_orderEgg_serv(orderEgg_id: int, orderEgg_update: OrderEggCreate, db: Session = Depends(get_db)):
    existing_orderEgg = read_orderEgg(orderEgg_id, db)
    if not existing_orderEgg:
        raise HTTPException(status_code=404, detail="OrderEgg not found")
    return update_orderEgg(orderEgg_id, orderEgg_update, db)

def delete_orderEgg_serv(orderEgg_id: int, db: Session = Depends(get_db)):
    return delete_orderEgg(orderEgg_id, db)