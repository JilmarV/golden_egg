from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import Depends, HTTPException
from Inventory.Inventory_Model import *
from Inventory.Inventory_Schema import *

# Creates a new product in the inventory
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

# Retrieves all products from the inventory
def read_inventory(db: Session = Depends(get_db)):
    inventories = db.query(Inventory).all()
    return inventories

# Retrieves a specific product from the inventory by its ID
def read_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return inventory

# Updates a product in the inventory in the database
def update_inventory(inventory_id: int, inventory_update: create_inventory, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in inventory_update.dict(exclude_unset=True).items():
        setattr(inventory, key, value)
    
    db.commit()
    db.refresh(inventory)
    return inventory

# Deletes a product from the inventory in the database
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(inventory)
    db.commit()
    return {"message": "Product deleted successfully"}
