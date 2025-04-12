from sqlalchemy.orm import Session
from models.Supplier import Supplier
from schemas.Supplier_Schema import SupplierCreate


def create_Supplier(db: Session, supplier: SupplierCreate):
    db_Supplier = Supplier(**supplier.dict())
    db.add(db_Supplier)
    db.commit()
    db.refresh(db_Supplier)
    return db_Supplier

def get_Supplier(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()