from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from OrderEgg.OrderEgg_Model import *
from OrderEgg.OrderEgg_Schema import *
from OrderEgg.OrderEgg_Service import *

router = APIRouter()

@router.post("/orderEgg/", status_code=201, response_model=OrderEggResponse)
def create_orderEgg_route(orderEgg: OrderEggCreate, db: Session = Depends(get_db)):
    return create_orderEgg_serv(orderEgg, db)

@router.get("/orderEgg/{orderEgg_id}")
def get_orderEgg_route(orderEgg_id: int, db: Session = Depends(get_db)):
    return read_orderEgg_serv(orderEgg_id, db)

@router.delete("/orderEgg/{orderEgg_id}")
def delete_orderEgg_route(orderEgg_id: int, db: Session = Depends(get_db)):
    return delete_orderEgg_serv(orderEgg_id, db)

@router.get("/orderEgg/")
def read_orderEggs_route(orderEgg_id: int, db: Session = Depends(get_db)):
    return read_orderEggs_serv(db)