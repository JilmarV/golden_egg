from sqlalchemy.orm import Session
from repositories.Inventory_Repository import create_Inventory, get_Inventory
from schemas.Inventory_Schema import InventoryCreate


def create_new_inventory(db: Session, inventory: InventoryCreate):
    return create_Inventory(db, inventory)


def fetch_inventory(db: Session, inventory_id: int):
    return get_Inventory(db, inventory_id)