"""Repository module for Bill operations."""

# pylint: disable=no-name-in-module

from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.Bill.bill_model import Bill
from app.Bill.bill_schema import BillCreate
from app.Order.order_model import Order
from app.User.user_model import User
from app.Role.role_model import Role


# Create a new bill in database
def create_bill(bill: BillCreate, db: Session):
    """Create a new bill record in the database."""
    db_bill = Bill(**bill.model_dump())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill


# Retrieves all bills from the database
def get_all_bills(db: Session):
    """Retrieve all bill records from the database."""
    bills = db.query(Bill).all()
    return bills


# Retrieves a specific bill garden by its ID
def get_bill_by_id(bill_id: int, db: Session):
    """Retrieve a specific bill record by its ID."""
    bill = db.query(Bill).filter(Bill.id == bill_id).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


# Updates a specific bill in the database
def update_bill(bill_id: int, bill: BillCreate, db: Session):
    """Update a specific bill record by its ID."""
    db_bill = db.query(Bill).filter(Bill.id == bill_id).first()

    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    for key, value in bill.model_dump().items():
        setattr(db_bill, key, value)
    db.commit()
    db.refresh(db_bill)
    return db_bill


# Deletes a specific bill from the database
def delete_bill(bill_id: int, db: Session):
    """Delete a specific bill record by its ID."""
    db_bill = db.query(Bill).filter(Bill.id == bill_id).first()

    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    db.delete(db_bill)
    db.commit()
    return {"message": "Bill deleted successfully"}


# Counts the number of bills for users with role 'CUSTOMER' issued within a date range
def count_customer_bills_in_range(start, end, db: Session):
    """
    Counts the number of bills for users with the role 'CUSTOMER'
    between the given start and end dates.
    """
    count = (
        db.query(Bill)  # pylint: disable=not-callable
        .join(Bill.order)
        .join(Order.user)
        .join(User.roles)
        .filter(
            Bill.issueDate >= start,
            Bill.issueDate <= end,
            Role.name == "CUSTOMER",
        )
        .all()
    )
    print(count)
    return count


def get_best_customer_of_month(start, end, db: Session) -> str:
    """
    Retrieves the best customer of the month based on the number of bills issued.
    """
    best_customer = (
        db.query(User)
        .join(User.roles)
        .join(User.orders)
        .join(Order.bill)
        .filter(
            Bill.issueDate >= start,
            Bill.issueDate <= end,
            Role.name == "CUSTOMER"
        )
        .group_by(User.id)
        .order_by(func.count(Bill.id).desc()) 
        .first()
    )


    return best_customer.name if best_customer else None


def get_all_bills_for_company(db: Session):
    """
    Retrieves all bills for users with specific roles.
    This function filters bills based on the roles of the users associated with them.
    """
    roles_to_filter = ["EMPLOYEE", "ADMIN"]

    bills = (
        db.query(Bill)
        .join(Bill.order)
        .join(Order.user)
        .join(User.roles)
        .filter(Role.name.in_(roles_to_filter))
        .all()
    )
    return bills


def get_all_bills_for_customers(db: Session):
    """
    Retrieves all bills for users with the 'CUSTOMER' role.

    Args:
        db (Session): The database session dependency.

    Returns:
        List: A list of bills associated with customers.
    """
    bills = (
        db.query(Bill)
        .join(Bill.order)
        .join(Order.user)
        .join(User.roles)
        .filter(Role.name == "CUSTOMER")
        .all()
    )
    return bills


def get_monthly_sales_total(start, end, db: Session) -> float:
    """
    Calculates the total amount of sales for bills within a given date range.
    Only considers bills from customers (users with the 'CUSTOMER' role).

    Args:
        start (datetime): The start date of the period.
        end (datetime): The end date of the period.
        db (Session): The database session dependency.

    Returns:
        float: The total sales amount for the specified period.
    """
    total_amount = (
        db.query(func.sum(Bill.totalprice))  # pylint: disable=not-callable
        .join(Bill.order)
        .join(Order.user)
        .join(User.roles)
        .filter(
            Bill.issueDate >= start,
            Bill.issueDate <= end,
            func.lower(Role.name) == "CUSTOMER",
        )
        .scalar()
    )
    return total_amount or 0.0
