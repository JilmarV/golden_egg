from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.Supplier import Supplier
from app.schemas.Supplier_Schema import SupplierCreate, SupplierUpdate

class SupplierRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_supplier(self, supplier_id: int) -> Optional[Supplier]:
        return self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

    def get_suppliers(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        return self.db.query(Supplier).offset(skip).limit(limit).all()

    def create_supplier(self, supplier: SupplierCreate) -> Supplier:
        db_supplier = Supplier(**supplier.model_dump())
        self.db.add(db_supplier)
        self.db.commit()
        self.db.refresh(db_supplier)
        return db_supplier

    def update_supplier(self, supplier_id: int, supplier: SupplierUpdate) -> Optional[Supplier]:
        db_supplier = self.get_supplier(supplier_id)
        if db_supplier:
            update_data = supplier.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_supplier, field, value)
            self.db.commit()
            self.db.refresh(db_supplier)
        return db_supplier

    def delete_supplier(self, supplier_id: int) -> bool:
        db_supplier = self.get_supplier(supplier_id)
        if db_supplier:
            self.db.delete(db_supplier)
            self.db.commit()
            return True
        return False