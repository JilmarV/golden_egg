"""Service layer for supplier operations."""

from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException
from app.Supplier.supplier_schema import SupplierCreate
from app.Supplier.supplier_repository import (
    create_supplier,
    read_suppliers,
    read_supplier,
    update_supplier,
    delete_supplier,
    check_previous_supplier,
)
from app.db.session import get_db


def create_supplier_serv(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """Creates a new supplier with field validation and duplication checks."""

    if not supplier.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")

    if not supplier.address.strip():
        raise HTTPException(status_code=400, detail="Address is required")

    if check_previous_supplier(db, "address", supplier.address.strip()):
        raise HTTPException(status_code=400, detail="Address already exists")

    return create_supplier(supplier, db)


def read_suppliers_serv(db: Session = Depends(get_db)):
    """Retrieves all suppliers."""
    return read_suppliers(db)


def read_supplier_serv(supplier_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific supplier by ID."""
    return read_supplier(supplier_id, db)


def update_supplier_serv(
    supplier_id: int,
    supplier_update: SupplierCreate,
    db: Session = Depends(get_db),
):
    """Updates a supplier by ID."""
    if not supplier_update.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")

    if not supplier_update.address.strip():
        raise HTTPException(status_code=400, detail="Address is required")

    if check_previous_supplier(db, "address", supplier_update.address.strip()):
        raise HTTPException(status_code=400, detail="Address already exists")
    return update_supplier(supplier_id, supplier_update, db)


def delete_supplier_serv(supplier_id: int, db: Session = Depends(get_db)):
    """Deletes a supplier by ID."""
    return delete_supplier(supplier_id, db)
