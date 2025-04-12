from sqlalchemy.orm import Session
from repositories.Supplier_Repository import create_Supplier, get_Supplier
from schemas.Supplier_Schema import SupplierCreate


def create_new_supplier(db: Session, supplier: SupplierCreate):
    return create_Supplier(db, supplier)


def fetch_supplier(db: Session, supplier_id: int):
    return get_Supplier(db, supplier_id)