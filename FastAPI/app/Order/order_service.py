"""Service module for Order operations."""

# pylint: disable=no-name-in-module

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.Order.order_repository import (
    create_order,
    delete_order,
    get_orders_in_current_month,
    read_order,
    read_orders,
    update_order,
    read_orders_by_month,
)
from app.Order.order_schema import OrderCreate
from app.User.user_model import User
from app.db.session import get_db


def read_orders_serv(db: Session):
    """Retrieve all orders from the database."""
    return read_orders(db)


def read_order_serv(order_id: int, db: Session = Depends(get_db)):
    """Retrieve a single order by ID, or raise 404 if not found."""
    return read_order(order_id, db)


def create_order_serv(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order after validating that user exists."""
    return create_order(order, db)


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


def get_orders_by_month_serv(
    year: int, month: int, db: Session = Depends(get_db)
) -> float:
    """Get all orders in a specific month."""
    return read_orders_by_month(db, year, month)


def get_orders_in_current_month_serv(db: Session = Depends(get_db)):
    """Get all orders in the current month."""
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return get_orders_in_current_month(db, start, end)


def count_orders_in_current_month_serv(db: Session = Depends(get_db)):
    """Count all orders in the current month."""
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return len(get_orders_in_current_month(db, start, end))
