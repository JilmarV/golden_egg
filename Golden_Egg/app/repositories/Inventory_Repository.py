from sqlalchemy.orm import Session
from models.Inventory import Inventory
from schemas.Inventory_Schema import InventoryCreate


def create_Inventory(db: Session, inventory: InventoryCreate):
    db_Inventory = Inventory(**inventory.dict())
    db.add(db_Inventory)
    db.commit()
    db.refresh(db_Inventory)
    return db_Inventory

def get_Inventory(db: Session, inventory_id: int):
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()