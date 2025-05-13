"""Router module for Egg endpoints."""

# pylint: disable=import-error, no-name-in-module

from sqlalchemy.orm import Session

from app.db.session import get_db

from fastapi import APIRouter, Depends
from fastapi.app.Bill.bill_schema import BillCreate, BillResponse
from fastapi.app.Bill.bill_service import (
    create_bill_serv,
    delete_bill_serv,
    read_bill_serv,
    read_bills_serv,
    update_bill_serv,
)

router = APIRouter()


# Endpoint to create a new bill
@router.post("/bill/", status_code=201, response_model=BillResponse)
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
@router.get("/bill/{bill_id}")
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
@router.get("/bill/")
def read_bills_route(db: Session = Depends(get_db)):
    """
    Handles the HTTP GET request to retrieve all bills.

    Args:
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        List[Bill]: A list of bills retrieved from the database.
    """
    return read_bills_serv(db)


# Endpoint to delete a specific bill by its ID
@router.delete("/bill/{bill_id}")
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
@router.put("/bill/{bill_id}")
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
