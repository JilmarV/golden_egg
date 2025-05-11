from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.Order.Order_Model import *
from app.Order.Order_Schema import *
from app.Order.Order_Service import *

router = APIRouter()

@router.post("/order/", status_code=201, response_model=OrderResponse)
def create_order_route(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Handles the creation of a new order.

    Args:
        order (OrderCreate): The data required to create a new order.
        db (Session, optional): The database session dependency. Defaults to the result of `Depends(get_db)`.

    Returns:
        The result of the `create_order_serv` function, which processes the creation of the order.
    """
    return create_order_serv(order, db)

@router.get("/order/{order_id}")
def get_order_route(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieve order details by order ID.

    Args:
        order_id (int): The unique identifier of the order to retrieve.
        db (Session, optional): The database session dependency. Defaults to the result of `get_db`.

    Returns:
        dict: The details of the requested order.

    Raises:
        HTTPException: If the order with the given ID is not found.
    """
    return read_order_serv(order_id, db)

@router.delete("/order/{order_id}")
def delete_order_route(order_id: int, db: Session = Depends(get_db)):
    """
    Deletes an order based on the provided order ID.

    Args:
        order_id (int): The ID of the order to be deleted.
        db (Session, optional): The database session dependency. Defaults to the session provided by `get_db`.

    Returns:
        Any: The result of the `delete_order_serv` service function, which handles the deletion logic.
    """
    return delete_order_serv(order_id, db)

@router.get("/order/")
def read_orders_route(order_id: int, db: Session = Depends(get_db)):
    """
    Handles the HTTP GET request to retrieve order details.

    Args:
        order_id (int): The ID of the order to retrieve.
        db (Session): Database session dependency, automatically provided by FastAPI.

    Returns:
        The result of the `read_orders_serv` function, which retrieves order details from the database.
    """
    return read_orders_serv(db)

@router.put("/order/{order_id}")
def update_order_route(order_id: int, order_update: OrderCreate, db: Session = Depends(get_db)):
    """
    Updates an existing order in the database.

    Args:
        order_id (int): The ID of the order to be updated.
        order_update (OrderCreate): An object containing the updated order details.
        db (Session, optional): The database session dependency. Defaults to the result of `Depends(get_db)`.

    Returns:
        The updated order object or the result of the update operation.
    """
    return update_order_serv(order_id, order_update, db)