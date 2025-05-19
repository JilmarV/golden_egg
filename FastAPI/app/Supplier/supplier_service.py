"""Service layer for supplier operations."""

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.Supplier.supplier_schema import SupplierCreate
from app.Supplier.supplier_repository import (
    create_supplier,
    read_suppliers,
    read_supplier,
    update_supplier,
    delete_supplier,
)
from fastapi import Depends


def create_supplier_serv(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """Creates a new supplier."""
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
