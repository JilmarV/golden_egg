from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db
from Inventory.Inventory_Schema import *
from Inventory.Inventory_Repository import *

# Service function to get a list of all inventory items
# It calls the read_inventory function with the database session
def read_inventory_serv(db: Session = Depends(get_db)):
    return read_inventory(db)

# Service function to get a specific product from the inventory by its ID
# It calls the read_inventory_item function with the inventory ID and database session
def read_inventory_item_serv(inventory_id: int, db: Session = Depends(get_db)):
    return read_inventory_item(inventory_id, db)

# Service function to create a new product in the inventory
# It calls the create_inventory function with the product data and the database session
def create_inventory_serv(inventory: InventoryCreate, db: Session = Depends(get_db)):
    return create_inventory(inventory, db)

# Service function to delete a product from the inventory by its ID
# It calls the delete_inventory function with the inventory ID and database session
def delete_inventory_serv(inventory_id: int, db: Session = Depends(get_db)):
    return delete_inventory(inventory_id, db)

# Service function to update a product's information in the inventory by its ID
# It calls the update_inventory function with the inventory ID, updated data, and the database session
def update_inventory_serv(inventory_id: int, inventory_update: create_inventory, db: Session = Depends(get_db)):
    return update_inventory(inventory_id, inventory_update, db)
