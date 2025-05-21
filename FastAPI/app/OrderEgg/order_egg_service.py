"""Service module for OrderEgg operations."""

# pylint: disable=no-name-in-module

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.OrderEgg.order_egg_repository import (
    read_order_eggs,
    read_order_egg,
    create_order_egg,
    update_order_egg,
    delete_order_egg,
)
from app.OrderEgg.order_egg_schema import OrderEggCreate
from app.db.session import get_db
from app.Order.order_model import Order
from app.Egg.egg_model import Egg


def read_order_eggs_serv(db: Session):
    """Retrieve all order eggs from the database."""
    return read_order_eggs(db)


def read_order_egg_serv(order_egg_id: int, db: Session = Depends(get_db)):
    """Retrieve a single order egg by ID, or raise 404 if not found."""
    return read_order_egg(order_egg_id, db)


def create_order_egg_serv(order_egg: OrderEggCreate, db: Session = Depends(get_db)):
    """Create a new order egg after validating that user and order exist."""
    if order_egg.quantity <= 0:
        raise HTTPException(
            status_code=400, detail="the amount of has to be greater than or equal to 0"
        )
    if order_egg.unit_price <=  0:
        raise HTTPException(
            status_code=400, detail=" the unit price must be greater than 0"
        )
    if order_egg.sub_total <=  0:
        raise HTTPException(
            status_code=400, detail=" the sub total must be greater than 0"
        )
    return create_order_egg(order_egg, db)


def update_order_egg_serv(
    order_egg_id: int, order_egg_update: OrderEggCreate, db: Session = Depends(get_db)
):
    """Update an existing order egg after validating that user and order exist."""
    existing_order_egg = read_order_egg(order_egg_id, db)
    if not existing_order_egg:
        raise HTTPException(status_code=404, detail="OrderEgg not found")
    if existing_order_egg.quantity <= 0:
        raise HTTPException(
            status_code=400, detail="the amount of has to be greater than or equal to 0"
        )
    if existing_order_egg.unit_price <=  0:
        raise HTTPException(
            status_code=400, detail=" the unit price must be greater than 0"
        )
    if existing_order_egg.sub_total <=  0:
        raise HTTPException(
            status_code=400, detail=" the sub total must be greater than 0"
        )
    return update_order_egg(order_egg_id, order_egg_update, db)


def delete_order_egg_serv(order_egg_id: int, db: Session = Depends(get_db)):
    """Delete an order egg by ID, or raise 404 if not found."""
    return delete_order_egg(order_egg_id, db)
