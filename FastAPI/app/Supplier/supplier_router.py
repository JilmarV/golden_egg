"""API Router for supplier endpoints."""

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


@router.post("/", status_code=201, response_model=SupplierResponse)
def create_supplier_route(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """
    Creates a new supplier using the provided supplier data.

    Args:
        supplier (SupplierCreate): The supplier data to create a new supplier.
        db (Session, optional): The database session dependency.

    Returns:
        The created supplier object or the result of the supplier creation service.
    """
    return create_supplier_serv(supplier, db)


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier_route(supplier_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a supplier by its ID.

    Args:
        supplier_id (int): The unique identifier of the supplier to retrieve.
        db (Session, optional): SQLAlchemy database session dependency.

    Returns:
        Supplier: The supplier object corresponding to the given ID.

    Raises:
        HTTPException: If the supplier with the specified ID does not exist.
    """
    return read_supplier_serv(supplier_id, db)


@router.delete("/{supplier_id}")
def delete_supplier_route(supplier_id: int, db: Session = Depends(get_db)):
    """
    Deletes a supplier by its ID.

    Args:
        supplier_id (int): The unique identifier of the supplier to be deleted.
        db (Session, optional): SQLAlchemy database session dependency.

    Returns:
        The result of the delete_supplier_serv function, which typically indicates
        success or failure of the deletion operation.
    """
    return delete_supplier_serv(supplier_id, db)


@router.get("/", response_model=list[SupplierResponse])
def read_suppliers_route(db: Session = Depends(get_db)):
    """
    Retrieve a list of suppliers from the database.

    Args:
        db (Session, optional): SQLAlchemy database session dependency. Defaults to Depends(get_db).

    Returns:
        List[Supplier]: A list of supplier objects retrieved from the database.
    """
    return read_suppliers_serv(db)


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier_route(
    supplier_id: int,
    supplier_update: SupplierCreate,
    db: Session = Depends(get_db),
):
    """
    Updates an existing supplier by its ID.
    Args:
        supplier_id (int): The unique identifier of the supplier to update.
        supplier_update (SupplierCreate): The updated supplier data.
        db (Session, optional): SQLAlchemy database session dependency.
    Returns:
        Supplier: The updated supplier object.
    Raises:
        HTTPException: If the supplier with the specified ID does not exist.
    """
    return update_supplier_serv(supplier_id, supplier_update, db)
