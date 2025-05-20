"""Router module for Order endpoints."""

from typing import List
from pytest import Session
from fastapi import APIRouter, Depends
from app.Order.order_schema import OrderCreate, OrderResponse
from app.Order.order_service import (
    create_order_serv,
    read_order_serv,
    delete_order_serv,
    read_orders_serv,
    update_order_serv,
    get_orders_by_month_serv,
)
from app.db.session import (
    get_db,
)

router = APIRouter()


@router.post("/", status_code=201, response_model=OrderResponse)
def create_order_route(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Handles the creation of a new order.

    Args:
        order (OrderCreate): The data required to create a new order.
        db (Session, optional): The database session dependency.
        Defaults to the result of `Depends(get_db)`.

    Returns:
        The result of the `create_order_serv` function,
        which processes the creation of the order.
    """
    return create_order_serv(order, db)


@router.get("/{order_id}")
def get_order_route(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieve order details by order ID.

    Args:
        order_id (int): The unique identifier of the order to retrieve.
        db (Session, optional): The database session dependency.
        Defaults to the result of `get_db`.

    Returns:
        dict: The details of the requested order.

    Raises:
        HTTPException: If the order with the given ID is not found.
    """
    return read_order_serv(order_id, db)


@router.delete("/{order_id}")
def delete_order_route(order_id: int, db: Session = Depends(get_db)):
    """
    Deletes an order based on the provided order ID.

    Args:
        order_id (int): The ID of the order to be deleted.
        db (Session, optional): The database session dependency.
        Defaults to the session provided by `get_db`.

    Returns:
        Any: The result of the `delete_order_serv` service function,
        which handles the deletion logic.
    """
    return delete_order_serv(order_id, db)


@router.get("/")
def read_orders_route(db: Session = Depends(get_db)):
    """
    Handles the HTTP GET request to retrieve order details.

    Args:
        order_id (int): The ID of the order to retrieve.
        db (Session): Database session dependency,
        automatically provided by

    Returns:
        The result of the `read_orders_serv` function,
        which retrieves order details from the database.
    """
    return read_orders_serv(db)


@router.put("/{order_id}", status_code=200)
def update_order_route(
    order_id: int, order_update: OrderCreate, db: Session = Depends(get_db)
):
    """
    Updates an existing order in the database.

    Args:
        order_id (int): The ID of the order to be updated.
        order_update (OrderCreate): An object containing the updated order details.
        db (Session, optional): The database session dependency.
        Defaults to the result of `Depends(get_db)`.

    Returns:
        The updated order object or the result of the update operation.
    """
    return update_order_serv(order_id, order_update, db)

#Añadir de donde saca el año y mes
@router.get("/search/totalOrdersMonth", response_model=List[OrderResponse])
def total_orders_by_month_route(year: int, month: int, db: Session = Depends(get_db)):
    """
    Retrieves the total number of orders for a specific month.
    Args:
        year (int): The year for which to retrieve the total orders.
        month (int): The month for which to retrieve the total orders.
        db (Session, optional): The database session dependency.
        Defaults to the session provided by `get_db`.
    Returns:
        float: The total number of orders for the specified month.
    """
    return get_orders_by_month_serv(year, month, db)
