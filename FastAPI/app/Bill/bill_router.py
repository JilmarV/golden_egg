"""Router module for Bill endpoints."""

from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import APIRouter, Depends
from typing import List
from app.User.user_schema import UserResponse
from app.Bill.bill_schema import BillCreate
from app.Bill.bill_schema import BillResponse
from app.Bill.bill_service import (
    count_customer_bills_current_month_serv,
    create_bill_serv,
    delete_bill_serv,
    get_all_bills_for_company_serv,
    get_all_bills_for_customers_serv,
    get_best_customer_of_month_serv,
    get_monthly_sales_total_serv,
    read_bill_serv,
    read_bills_serv,
    update_bill_serv,
)

router = APIRouter()


# Endpoint to create a new bill
@router.post("/", status_code=201, response_model=BillResponse)
def create_bill_route(bill: BillCreate, db: Session = Depends(get_db)):
    """
    Creates a new bill using the provided bill data and database session.

    Args:
        bill (BillCreate): The data required to create a new bill.
        db (Session): The database session dependency.

    Returns:
        The created bill object.
    """
    return create_bill_serv(bill, db)


# Endpoint to retrieve a specific bill by its ID
@router.get("/{bill_id}", response_model=BillResponse)
def get_bill_route(bill_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a bill by its ID.

    Args:
        bill_id (int): The unique identifier of the bill to retrieve.
        db (Session, optional): The database session dependency.
        Defaults to the session provided by `get_db`.

    Returns:
        The bill data retrieved by the `read_bill_serv` service function.
    """
    return read_bill_serv(bill_id, db)


# Endpoint to retrieve all bills
@router.get("/", response_model= List[BillResponse])
def read_bills_route(db: Session = Depends(get_db)):
    """
    Handles the HTTP GET request to retrieve all bills.

    Args:
        db (Session): Database session dependency injected by

    Returns:
        List[Bill]: A list of bills retrieved from the database.
    """
    return read_bills_serv(db)


# Endpoint to delete a specific bill by its ID
@router.delete("/{bill_id}")
def delete_bill_route(bill_id: int, db: Session = Depends(get_db)):
    """
    Deletes a bill record from the database.

    Args:
        bill_id (int): The unique identifier of the bill to be deleted.
        db (Session): The database session dependency.

    Returns:
        The result of the delete operation, typically indicating success or failure.
    """
    return delete_bill_serv(bill_id, db)


# Endpoint to update a specific bill by its ID
@router.put("/{bill_id}")
def update_bill_route(
    bill_id: int, bill_update: BillCreate, db: Session = Depends(get_db)
):
    """
    Updates an existing bill with the provided data.

    Args:
        bill_id (int): The ID of the bill to be updated.
        bill_update (BillCreate): The data to update the bill with.
        db (Session, optional): The database session dependency.
        Defaults to the result of `Depends(get_db)`.

    Returns:
        The updated bill object or the result of the update operation.
    """
    return update_bill_serv(bill_id, bill_update, db)


@router.get("/customer/countThisMonth")
def get_customer_bills_count_route(db: Session = Depends(get_db)):
    """
    Retrieve the count of bills associated with a customer.

    Args:
        db (Session, optional): SQLAlchemy database session.
        Automatically injected by FastAPI dependency.

    Returns:
        int: The number of bills for the customer.
    """
    return count_customer_bills_current_month_serv(db)


@router.get("/customer/bestCustomer")
def get_best_customer_route(db: Session = Depends(get_db), response_model=UserResponse):
    """
    Retrieve the best customer based on the number of bills.

    Args:
        db (Session, optional): SQLAlchemy database session.
        Automatically injected by FastAPI dependency.

    Returns:
        dict: The best customer and their bill count.
    """
    return get_best_customer_of_month_serv(db)


@router.get("/company/getAllOfCompany", response_model= List[BillResponse])
def get_all_bills_of_company_route(db: Session = Depends(get_db), response_model=list):
    """
    Retrieve all bills associated with a company.

    This route handler fetches and returns the count of customer bills
    for a company from the database.

    Args:
        db (Session, optional): SQLAlchemy database session dependency.
        Defaults to Depends(get_db).

    Returns:
        int: The count of customer bills for the company.
    """
    return get_all_bills_for_company_serv(db)


@router.get("/customer/getAllOfCustomers", response_model= List[BillResponse])
def get_all_customer_bills_route(db: Session = Depends(get_db), response_model=list[BillResponse]):
    """
    Retrieve all bills associated with customers (users with the "CUSTOMER" role).

    Args:
        db (Session, optional): SQLAlchemy database session dependency.
        Defaults to Depends(get_db).

    Returns:
        List: A list of bills associated with customers.
    """
    return get_all_bills_for_customers_serv(db)


@router.get("/company/monthlySalesTotal")
def get_monthly_sales_total_route(db: Session = Depends(get_db)):
    """
    Retrieves the total amount of sales for the current month.
    Only bills from customers are considered in the calculation.

    Args:
        db (Session, optional): SQLAlchemy database session dependency.
        Defaults to Depends(get_db).

    Returns:
        float: The total monthly sales amount.
    """
    return get_monthly_sales_total_serv(db)
