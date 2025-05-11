from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi.app.Supplier.supplier_repository import *
from app.Supplier.Supplier_Service import *

router = APIRouter()

# Endpoint to create a new supplier
# Accepts a SupplierCreate object and returns a SupplierResponse with the created supplier
@router.post("/supplier/", status_code=201, response_model=SupplierResponse)
def create_supplier_route(supplier: SupplierCreate, db: Session = Depends(get_db)):
    return create_supplier_serv(supplier, db)

# Endpoint to get a specific supplier by its ID
# Returns the supplier matching the provided ID
@router.get("/supplier/{supplier_id}", response_model=SupplierResponse)
def get_supplier_route(supplier_id: int, db: Session = Depends(get_db)):
    return read_supplier_serv(supplier_id, db)

# Endpoint to delete a supplier by its ID
# Returns a success message once the supplier is deleted
@router.delete("/supplier/{supplier_id}")
def delete_supplier_route(supplier_id: int, db: Session = Depends(get_db)):
    return delete_supplier_serv(supplier_id, db)

# Endpoint to get a list of all suppliers
# Returns a list of suppliers
@router.get("/supplier/", response_model=list[SupplierResponse])
def read_suppliers_route(db: Session = Depends(get_db)):
    return read_suppliers_serv(db)

# Endpoint to update a supplier's information by its ID
# Accepts a SupplierCreate object with the updated data
@router.put("/supplier/{supplier_id}", response_model=SupplierResponse)
def update_supplier_route(supplier_id: int, supplier_update: SupplierCreate, db: Session = Depends(get_db)):
    return update_supplier_serv(supplier_id, supplier_update, db)
