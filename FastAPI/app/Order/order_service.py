"""Service module for Order operations."""

# pylint: disable=no-name-in-module

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.Order.order_repository import (
    create_order,
    delete_order,
    read_order,
    read_orders,
    update_order,
    read_orders_by_month,
)
from app.Order.order_schema import OrderCreate
from app.User.user_model import User


def read_orders_serv(db: Session):
    """Retrieve all orders from the database."""
    return read_orders(db)


def read_order_serv(order_id: int, db: Session):
    """Retrieve a single order by ID, or raise 404 if not found."""
    return read_order(order_id, db)


def create_order_serv(order: OrderCreate, db: Session):
    """Create a new order after validating that user exists."""
    if order.totalPrice <= 0:
        raise HTTPException(
            status_code=400, detail="the total price has to be greater than 0"
        )
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not order.state.strip():
        raise HTTPException(status_code=400, detail="Order is required")
    return create_order(order, db)


def update_order_serv(order_id: int, order_update: OrderCreate, db: Session):
    """Update an existing order after validating that user exists."""
    existing_order = read_order(order_id, db)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if existing_order.totalPrice <= 0:
        raise HTTPException(
            status_code=400, detail="the total price has to be greater than 0"
        )

    if not existing_order.state.strip():
        raise HTTPException(status_code=400, detail="Order is required")

    user = db.query(User).filter(User.id == order_update.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return update_order(order_id, order_update, db)


def delete_order_serv(order_id: int, db: Session):
    """Delete an order by ID, or raise 404 if not found."""
    return delete_order(order_id, db)


def get_orders_by_month_serv(year: int, month: int, db: Session):
    """Get all orders in a specific month."""
    return read_orders_by_month(db, year, month)

def count_orders_in_month_serv(year: int, month: int,db: Session):
    """Count all orders in the current month."""
    now = datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return len(read_orders_by_month(db, year, month))