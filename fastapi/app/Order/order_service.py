"""Service module for Order operations."""

# pylint: disable=no-name-in-module

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.app.Order.order_repository import (
    delete_order,
    read_order,
    read_orders,
    update_order,
)
from fastapi.app.Order.order_schema import OrderCreate
from fastapi.app.User.user_model import User
from fastapi.app.db.session import get_db


def read_orders_serv(db: Session):
    """Retrieve all orders from the database."""
    return read_orders(db)


def read_order_serv(order_id: int, db: Session = Depends(get_db)):
    """Retrieve a single order by ID, or raise 404 if not found."""
    return read_order(order_id, db)


def create_order_serv(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order after validating that user exists."""
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


def update_order_serv(
    order_id: int, order_update: OrderCreate, db: Session = Depends(get_db)
):
    """Update an existing order after validating that user exists."""
    existing_order = read_order(order_id, db)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    user = db.query(User).filter(User.id == order_update.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return update_order(order_id, order_update, db)


def delete_order_serv(order_id: int, db: Session = Depends(get_db)):
    """Delete an order by ID, or raise 404 if not found."""
    return delete_order(order_id, db)
