from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.Inventory import Inventory
from app.schemas.Inventory_Schema import InventoryCreate, InventoryUpdate

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_inventory_item(self, item_id: int) -> Optional[Inventory]:
        return self.db.query(Inventory).filter(Inventory.id == item_id).first()

    def get_inventory_by_supplier(self, supplier_id: int) -> List[Inventory]:
        return self.db.query(Inventory).filter(Inventory.supplier_id == supplier_id).all()

    def get_inventory_by_egg(self, egg_id: int) -> Optional[Inventory]:
        return self.db.query(Inventory).filter(Inventory.egg_id == egg_id).first()

    def get_all_inventory(self, skip: int = 0, limit: int = 100) -> List[Inventory]:
        return self.db.query(Inventory).offset(skip).limit(limit).all()

    def create_inventory_item(self, inventory: InventoryCreate) -> Inventory:
        db_inventory = Inventory(**inventory.model_dump())
        self.db.add(db_inventory)
        self.db.commit()
        self.db.refresh(db_inventory)
        return db_inventory

    def update_inventory_item(self, item_id: int, inventory: InventoryUpdate) -> Optional[Inventory]:
        db_inventory = self.get_inventory_item(item_id)
        if db_inventory:
            update_data = inventory.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_inventory, field, value)
            self.db.commit()
            self.db.refresh(db_inventory)
        return db_inventory

    def delete_inventory_item(self, item_id: int) -> bool:
        db_inventory = self.get_inventory_item(item_id)
        if db_inventory:
            self.db.delete(db_inventory)
            self.db.commit()
            return True
        return False