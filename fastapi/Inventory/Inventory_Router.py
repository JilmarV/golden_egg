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
    """
    Creates a new inventory entry by delegating the operation to the service layer.

    Args:
        inventory (InventoryCreate): The inventory data to be created, provided as an instance of the InventoryCreate schema.
        db (Session, optional): The database session dependency, automatically injected by FastAPI.

    Returns:
        The result of the inventory creation operation, as returned by the service layer.
    """
    return create_inventory_serv(inventory, db)

# Endpoint to get a specific product from the inventory by its ID
# Returns the product matching the provided ID
@router.get("/inventory/{inventory_id}", response_model=InventoryResponse)
def get_inventory_item_route(inventory_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific inventory item by its ID.

    Args:
        inventory_id (int): The unique identifier of the inventory item to retrieve.
        db (Session, optional): The database session dependency, automatically provided by FastAPI.

    Returns:
        The inventory item data retrieved from the database.

    Raises:
        HTTPException: If the inventory item with the given ID is not found.
    """
    return read_inventory_item_serv(inventory_id, db)

# Endpoint to delete a product from the inventory by its ID
# Returns a success message once the product is deleted
@router.delete("/inventory/{inventory_id}", response_model=dict)
def delete_inventory_route(inventory_id: int, db: Session = Depends(get_db)):
    """
    Deletes an inventory item based on the provided inventory ID.

    Args:
        inventory_id (int): The ID of the inventory item to be deleted.
        db (Session, optional): The database session dependency. Defaults to the session provided by `get_db`.

    Returns:
        Any: The result of the inventory deletion operation, as returned by the `delete_inventory_serv` service function.
    """
    return delete_inventory_serv(inventory_id, db)

# Endpoint to get a list of all products in the inventory
# Returns a list of products
@router.get("/inventory/", response_model=list[InventoryResponse])
def read_inventory_route(db: Session = Depends(get_db)):
    """
    Handles the HTTP request to read the inventory.

    This function acts as a FastAPI route handler for retrieving inventory data.
    It depends on a database session, which is provided by the `get_db` dependency.

    Args:
        db (Session): A SQLAlchemy database session provided by the dependency injection.

    Returns:
        The result of the `read_inventory_serv` function, which retrieves the inventory data.
    """
    return read_inventory_serv(db)

# Endpoint to update a product's information in the inventory by its ID
# Accepts an InventoryUpdate object with the updated data
@router.put("/inventory/{inventory_id}", response_model=InventoryResponse)
def update_inventory_route(inventory_id: int, inventory_update: InventoryCreate, db: Session = Depends(get_db)):
    """
    Updates an inventory item in the database.

    Args:
        inventory_id (int): The unique identifier of the inventory item to be updated.
        inventory_update (InventoryCreate): The data object containing the updated inventory details.
        db (Session): The database session dependency.

    Returns:
        The updated inventory item after applying the changes.
    """
    return update_inventory_serv(inventory_id, inventory_update, db)
