"""Repository module for OrderEgg operations."""

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.OrderEgg.order_egg_model import OrderEgg
from app.OrderEgg.order_egg_schema import OrderEggCreate
from app.db.session import get_db


def create_order_egg(order_egg: OrderEggCreate, db: Session):
    """
    Creates a new order egg record in the database.

    Args:
        order_egg (OrderEggCreate): The data required to create a new order egg.
        db (Session): The database session used to interact with the database.

    Returns:
        OrderEgg: The newly created order egg record.
    """
    db_order_egg = OrderEgg(**order_egg.model_dump())
    db.add(db_order_egg)
    db.commit()
    db.refresh(db_order_egg)
    return db_order_egg


def read_order_eggs(db: Session = Depends(get_db)):
    """
    Fetches all OrderEgg records from the database.

    Args:
        db (Session): The database session dependency.

    Returns:
        list: A list of all OrderEgg objects retrieved from the database.
    """
    order_eggs = db.query(OrderEgg).all()
    return order_eggs


def read_order_egg(order_egg_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an OrderEgg record by its ID.

    Args:
        order_egg_id (int): The ID of the OrderEgg to retrieve.
        db (Session): The database session dependency.

    Returns:
        OrderEgg: The retrieved OrderEgg record.

    Raises:
        HTTPException: If no OrderEgg is found with the given ID, raises a 404 error.
    """
    order_egg = db.query(OrderEgg).filter(OrderEgg.id == order_egg_id).first()
    if order_egg is None:
        raise HTTPException(status_code=404, detail="OrderEgg not found")
    return order_egg


def delete_order_egg(order_egg_id: int, db: Session = Depends(get_db)):
    """
    Deletes an OrderEgg record from the database based on the provided order_egg_id.

    Args:
        order_egg_id (int): The ID of the OrderEgg to be deleted.
        db (Session): The database session dependency.

    Raises:
        HTTPException: If the OrderEgg with the given ID is not found, a 404 error is raised.

    Returns:
        model_dump: A model_dumpionary containing a success message indicating the OrderEgg was deleted.
    """
    order_egg = db.query(OrderEgg).filter(OrderEgg.id == order_egg_id).first()
    if order_egg is None:
        raise HTTPException(status_code=404, detail="OrderEgg not found")
    db.delete(order_egg)
    db.commit()
    return {"message": "Order_egg deleted successfully"}


def update_order_egg(
    order_egg_id: int, order_egg_update: OrderEggCreate, db: Session = Depends(get_db)
):
    """
    Updates an existing OrderEgg record in the database.

    Args:
        order_egg_id (int): The ID of the OrderEgg to update.
        order_egg_update (OrderEggCreate): An object containing the updated data for the OrderEgg.
        db (Session): The database session dependency.

    Returns:
        OrderEgg: The updated OrderEgg object.

    Raises:
        HTTPException: If the OrderEgg with the given ID is not found, raises a 404 error.
    """
    order_egg = db.query(OrderEgg).filter(OrderEgg.id == order_egg_id).first()
    if order_egg is None:
        raise HTTPException(status_code=404, detail="OrderEgg not found")

    for key, value in order_egg_update.model_dump(exclude_unset=True).items():
        setattr(order_egg, key, value)

    db.commit()
    db.refresh(order_egg)
    return order_egg
