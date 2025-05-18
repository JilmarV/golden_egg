"""Repository functions for managing supplier data in the database."""

from sqlalchemy.orm import Session

from FastAPI.app.db.session import get_db
from FastAPI.app.Supplier.supplier_model import Supplier
from FastAPI.app.Supplier.supplier_schema import SupplierCreate

from fastapi import HTTPException, Depends


def create_supplier(supplier: SupplierCreate, db: Session):
    """Creates a new supplier."""
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def read_suppliers(db: Session = Depends(get_db)):
    """Retrieves all suppliers."""
    return db.query(Supplier).all()


def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific supplier by ID."""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


def update_supplier(
    supplier_id: int,
    supplier_update: SupplierCreate,
    db: Session = Depends(get_db),
):
    """Updates an existing supplier by ID."""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    for key, value in supplier_update.dict(exclude_unset=True).items():
        setattr(supplier, key, value)

    db.commit()
    db.refresh(supplier)
    return supplier


def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """Deletes a supplier by ID."""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(supplier)
    db.commit()
    return {"message": "Supplier deleted successfully"}
