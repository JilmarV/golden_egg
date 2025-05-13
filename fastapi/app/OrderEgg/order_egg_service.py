"""Service module for OrderEgg operations."""

# pylint: disable=no-name-in-module

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.app.OrderEgg.order_egg_repository import (
    read_order_eggs,
    read_order_egg,
    create_order_egg,
    update_order_egg,
    delete_order_egg,
)
from fastapi.app.OrderEgg.order_egg_schema import OrderEggCreate
from fastapi.app.db.session import get_db


def read_order_eggs_serv(db: Session):
    """Retrieve all order eggs from the database."""
    return read_order_eggs(db)


def read_order_egg_serv(order_egg_id: int, db: Session = Depends(get_db)):
    """Retrieve a single order egg by ID, or raise 404 if not found."""
    return read_order_egg(order_egg_id, db)


def create_order_egg_serv(order_egg: OrderEggCreate, db: Session = Depends(get_db)):
    """Create a new order egg after validating that user and order exist."""
    return create_order_egg(order_egg, db)


def update_order_egg_serv(
    order_egg_id: int, order_egg_update: OrderEggCreate, db: Session = Depends(get_db)
):
    """Update an existing order egg after validating that user and order exist."""
    existing_order_egg = read_order_egg(order_egg_id, db)
    if not existing_order_egg:
        raise HTTPException(status_code=404, detail="OrderEgg not found")
    return update_order_egg(order_egg_id, order_egg_update, db)


def delete_order_egg_serv(order_egg_id: int, db: Session = Depends(get_db)):
    """Delete an order egg by ID, or raise 404 if not found."""
    return delete_order_egg(order_egg_id, db)
