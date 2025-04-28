from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from Inventory.Inventory_Model import *
from Inventory.Inventory_Schema import *
from Inventory.Inventory_Service import *

router = APIRouter()

# Endpoint to create a new product in the inventory
# Accepts an InventoryCreate object and returns an InventoryResponse with the created product
@router.post("/inventory/", status_code=201, response_model=InventoryResponse)
def create_inventory_route(inventory: InventoryCreate, db: Session = Depends(get_db)):
    return create_inventory_serv(inventory, db)

# Endpoint to get a specific product from the inventory by its ID
# Returns the product matching the provided ID
@router.get("/inventory/{inventory_id}", response_model=InventoryResponse)
def get_inventory_item_route(inventory_id: int, db: Session = Depends(get_db)):
    return read_inventory_item_serv(inventory_id, db)

# Endpoint to delete a product from the inventory by its ID
# Returns a success message once the product is deleted
@router.delete("/inventory/{inventory_id}", response_model=dict)
def delete_inventory_route(inventory_id: int, db: Session = Depends(get_db)):
    return delete_inventory_serv(inventory_id, db)

# Endpoint to get a list of all products in the inventory
# Returns a list of products
@router.get("/inventory/", response_model=list[InventoryResponse])
def read_inventory_route(db: Session = Depends(get_db)):
    return read_inventory_serv(db)

# Endpoint to update a product's information in the inventory by its ID
# Accepts an InventoryUpdate object with the updated data
@router.put("/inventory/{inventory_id}", response_model=InventoryResponse)
def update_inventory_route(inventory_id: int, inventory_update: InventoryCreate, db: Session = Depends(get_db)):
    return update_inventory_serv(inventory_id, inventory_update, db)
