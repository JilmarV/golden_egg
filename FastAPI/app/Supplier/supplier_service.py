"""Service layer for supplier operations."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.Supplier.supplier_schema import SupplierCreate
from app.Supplier.supplier_repository import (
    create_supplier,
    read_suppliers,
    read_supplier,
    update_supplier,
    delete_supplier,
    check_previous_supplier
)
from app.db.session import get_db
from fastapi import Depends


def create_supplier_serv(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """Creates a new supplier."""
    for attr in ["address"]:
        if check_previous_supplier(db, attr, getattr(supplier, attr)):
            raise HTTPException(status_code=400, detail=f"{attr.capitalize()} Supplier already exists")
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
    return update_supplier(supplier_id, supplier_update, db)


def delete_supplier_serv(supplier_id: int, db: Session = Depends(get_db)):
    """Deletes a supplier by ID."""
    return delete_supplier(supplier_id, db)
