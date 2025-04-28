from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from Order.Order_Model import *
from Order.Order_Schema import *
from Order.Order_Service import *

router = APIRouter()

@router.post("/order/", status_code=201, response_model=OrderResponse)
def create_order_route(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order_serv(order, db)

@router.get("/order/{order_id}")
def get_order_route(order_id: int, db: Session = Depends(get_db)):
    return read_order_serv(order_id, db)

@router.delete("/order/{order_id}")
def delete_order_route(order_id: int, db: Session = Depends(get_db)):
    return delete_order_serv(order_id, db)

@router.get("/order/")
def read_orders_route(order_id: int, db: Session = Depends(get_db)):
    return read_orders_serv(db)

@router.put("/order/{order_id}")
def update_order_route(order_id: int, order_update: OrderCreate, db: Session = Depends(get_db)):
    return update_order_serv(order_id, order_update, db)