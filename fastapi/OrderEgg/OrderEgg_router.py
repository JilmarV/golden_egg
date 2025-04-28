from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi.OrderEgg.OrderEgg_model import *
from fastapi.OrderEgg.OrderEgg_schema import OrderEggCreate, OrderEggResponse
from fastapi.OrderEgg.OrderEgg_service import create_orderEgg_serv, read_orderEgg_serv, read_orderEggs_serv, delete_orderEgg_serv

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