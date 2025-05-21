"""Repository module for Order operations."""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.Order.order_schema import OrderCreate
from app.Order.order_model import Order


def create_order(order: OrderCreate, db: Session):
    """Create a new order in the database.
    Args:
        order (OrderCreate): The order to create.
        db (Session): The database session.
    Returns:
        Order: The created order.
    """
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def read_orders(db: Session):
    """Get all orders from the database.
    Args:
        db (Session): The database session.
    Returns:
        List[Order]: A list of all orders.
    """
    orders = db.query(Order).all()
    return orders


def read_order(order_id: int, db: Session):
    """Get a specific order by ID from the database.
    Args:
        order_id (int): The ID of the order to retrieve.
        db (Session): The database session.
    Returns:
        Order: The order with the specified ID.
    Raises:
        HTTPException: If the order is not found.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def delete_order(order_id: int, db: Session):
    """Delete a specific order by ID from the database.
    Args:
        order_id (int): The ID of the order to delete.
        db (Session): The database session.
    Returns:
        model_dump: A message indicating the order was deleted successfully.
    Raises:
        HTTPException: If the order is not found.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}


def update_order(order_id: int, order_update: OrderCreate, db: Session):
    """Update a specific order by ID in the database.
    Args:
        order_id (int): The ID of the order to update.
        order_update (OrderCreate): The updated order data.
        db (Session): The database session.
    Returns:
        Order: The updated order.
    Raises:
        HTTPException: If the order is not found.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order_update.model_dump(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order


def read_orders_by_month(db: Session, year: int, month: int) -> float:
    """Get all orders in a specific month.
    Args:
        db (Session): The database session.
        year (int): The year of the month to filter.
        month (int): The month to filter.
    Returns:
        List[Order]: A list of orders in the specified month.
    """
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    return (
        db.query(Order)
        .filter(Order.orderDate >= start_date, Order.orderDate < end_date)
        .all()
    )