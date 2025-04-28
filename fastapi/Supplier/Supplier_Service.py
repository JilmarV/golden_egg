from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import Depends
from fastapi.Supplier.Supplier_Schema import *
from fastapi.Supplier.Supplier_Repository import *

# Service to create a new supplier
def create_supplier_serv(supplier: SupplierCreate, db: Session = Depends(get_db)):
    return create_supplier(supplier, db)

# Service to retrieve all suppliers
def read_suppliers_serv(db: Session = Depends(get_db)):
    return read_suppliers(db)

# Service to retrieve a specific supplier by ID
def read_supplier_serv(supplier_id: int, db: Session = Depends(get_db)):
    return read_supplier(supplier_id, db)

# Service to update a supplier by ID
def update_supplier_serv(supplier_id: int, supplier_update: SupplierCreate, db: Session = Depends(get_db)):
    return update_supplier(supplier_id, supplier_update, db)

# Service to delete a supplier by ID
def delete_supplier_serv(supplier_id: int, db: Session = Depends(get_db)):
    return delete_supplier(supplier_id, db)
