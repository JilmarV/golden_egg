"""Router module for OrderEgg endpoints."""

from fastapi import APIRouter, Depends
from pytest import Session
from app.OrderEgg.order_egg_schema import OrderEggCreate, OrderEggResponse
from app.OrderEgg.order_egg_service import (
    create_order_egg_serv,
    delete_order_egg_serv,
    read_order_egg_serv,
    read_order_eggs_serv,
    update_order_egg_serv,
)
from app.db.session import get_db

router = APIRouter()


@router.post("/", status_code=201, response_model=OrderEggResponse)
def create_order_egg_route(order_egg: OrderEggCreate, db: Session = Depends(get_db)):
    """
    Handles the creation of an order for eggs.

    Args:
        order_egg (OrderEggEggCreate): The data required to create a new egg order.
        db (Session, optional): The database session dependency.
        Defaults to the result of `Depends(get_db)`.

    Returns:
        The result of the `create_order_egg_serv` service function,
        which processes the creation of the egg order.
    """
    return create_order_egg_serv(order_egg, db)


@router.get("/{order_egg_id}")
def get_order_egg_route(order_egg_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the details of a specific order egg by its ID.

    Args:
        order_egg_id (int): The unique identifier of the order egg to retrieve.
        db (Session, optional): The database session dependency.
        Defaults to the session provided by `get_db`.

    Returns:
        The result of the `read_order_egg_serv` function,
        which contains the details of the specified order egg.
    """
    return read_order_egg_serv(order_egg_id, db)


@router.delete("/{order_egg_id}")
def delete_order_egg_route(order_egg_id: int, db: Session = Depends(get_db)):
    """
    Deletes an order egg record from the database.

    Args:
        order_egg_id (int): The ID of the order egg to be deleted.
        db (Session): The database session dependency.

    Returns:
        The result of the delete operation, as returned by the service layer.
    """
    return delete_order_egg_serv(order_egg_id, db)


@router.get("/")
def read_order_eggs_route(db: Session = Depends(get_db)):
    """
    Handles the HTTP GET request to retrieve all order eggs.

    Args:
        db (Session): Database session dependency injected by

    Returns:
        List[OrderEgg]: A list of order eggs retrieved from the database.
    """
    return read_order_eggs_serv(db)


@router.put("/{order_egg_id}")
def update_order_egg_route(
    order_egg_id: int,
    order_egg_update: OrderEggCreate,
    db: Session = Depends(get_db),
):
    """
    Updates an existing order egg record.

    Args:
        order_egg_id (int): The ID of the order egg to be updated.
        order_egg_update (OrderEggEggCreate): The data to update the order egg with.
        db (Session, optional): The database session dependency.

    Returns:
        The updated order egg record.
    """
    return update_order_egg_serv(order_egg_id, order_egg_update, db)
