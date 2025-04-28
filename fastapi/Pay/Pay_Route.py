from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from Pay_Model import *
from Pay_Schema import PayCreate, PayResponse
from Pay_Service import create_pay_serv, read_pay_serv, read_pays_serv, delete_pay_serv, update_pay_serv

router = APIRouter()

@router.post("/pay/", status_code=201, response_model=PayResponse)
def create_pay_route(pay: PayCreate, db: Session = Depends(get_db)):
    return create_pay_serv(pay, db)

@router.get("/pay/{pay_id}")
def get_pay_route(pay_id: int, db: Session = Depends(get_db)):
    return read_pay_serv(pay_id, db)

@router.delete("/pay/{pay_id}")
def delete_pay_route(pay_id: int, db: Session = Depends(get_db)):
    return delete_pay_serv(pay_id, db)

@router.get("/pay/")
def read_pays_route(pay_id: int, db: Session = Depends(get_db)):
    return read_pays_serv(db)

@router.put("/pay/{pay_id}")
def update_pay_route(pay_id: int, pay_update: PayCreate, db: Session = Depends(get_db)):
    return update_pay_serv(pay_id, pay_update, db)