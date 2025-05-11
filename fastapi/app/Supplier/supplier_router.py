"""API Router for supplier endpoints."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.Supplier.supplier_schema import SupplierCreate, SupplierResponse
from app.Supplier.supplier_service import (
    create_supplier_serv,
    read_supplier_serv,
    delete_supplier_serv,
    read_suppliers_serv,
    update_supplier_serv,
)
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/supplier/", status_code=201, response_model=SupplierResponse)
def create_supplier_route(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """Creates a new supplier."""
    return create_supplier_serv(supplier, db)


@router.get("/supplier/{supplier_id}", response_model=SupplierResponse)
def get_supplier_route(supplier_id: int, db: Session = Depends(get_db)):
    """Retrieves a supplier by ID."""
    return read_supplier_serv(supplier_id, db)


@router.delete("/supplier/{supplier_id}")
def delete_supplier_route(supplier_id: int, db: Session = Depends(get_db)):
    """Deletes a supplier by ID."""
    return delete_supplier_serv(supplier_id, db)


@router.get("/supplier/", response_model=list[SupplierResponse])
def read_suppliers_route(db: Session = Depends(get_db)):
    """Retrieves all suppliers."""
    return read_suppliers_serv(db)


@router.put("/supplier/{supplier_id}", response_model=SupplierResponse)
def update_supplier_route(
    supplier_id: int,
    supplier_update: SupplierCreate,
    db: Session = Depends(get_db),
):
    """Updates a supplier by ID."""
    return update_supplier_serv(supplier_id, supplier_update, db)
