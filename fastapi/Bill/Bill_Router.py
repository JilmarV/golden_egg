from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from Bill.Bill_Schema import *
from Bill_Service import *

router = APIRouter()

# Endpoint to create a new bill
@router.post("/bill/", status_code=201, response_model=BillResponse)
def create_bill_route(bill: BillCreate, db: Session = Depends(get_db)):
    return create_bill_serv(bill, db)

# Endpoint to retrieve a specific bill by its ID
@router.get("/bill/{bill_id}")
def get_bill_route(bill_id: int, db: Session = Depends(get_db)):
    return read_bill_serv(bill_id, db)

# Endpoint to retrieve all bills
@router.get("/bill/")
def read_bills_route(db: Session = Depends(get_db)):
    return read_bills_serv(db)

# Endpoint to delete a specific bill by its ID
@router.delete("/bill/{bill_id}")
def delete_bill_route(bill_id: int, db: Session = Depends(get_db)):
    return delete_bill_serv(bill_id, db)

# Endpoint to update a specific bill by its ID
@router.put("/bill/{bill_id}")
def update_bill_route(bill_id: int, bill_update: BillCreate, db: Session = Depends(get_db)):
    return update_bill_serv(bill_id, bill_update, db)