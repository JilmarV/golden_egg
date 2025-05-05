from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from Bill.Bill_Schema import *
from Bill.Bill_Service import *

router = APIRouter()

# Endpoint to create a new bill
@router.post("/bill/", status_code=201, response_model=BillResponse)
def create_bill_route(bill: BillCreate, db: Session = Depends(get_db)):
    """
    Handles the creation of a new bill.

    Args:
        bill (BillCreate): The data required to create a new bill, provided as a Pydantic model.
        db (Session): The database session dependency, automatically injected by FastAPI.

    Returns:
        The result of the bill creation service, which typically includes the created bill's details.
    """
    return create_bill_serv(bill, db)

# Endpoint to retrieve a specific bill by its ID
@router.get("/bill/{bill_id}")
def get_bill_route(bill_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a bill by its ID.

    Args:
        bill_id (int): The unique identifier of the bill to retrieve.
        db (Session, optional): The database session dependency. Defaults to the session provided by `get_db`.

    Returns:
        The bill data retrieved by the `read_bill_serv` service function.
    """
    return read_bill_serv(bill_id, db)

# Endpoint to retrieve all bills
@router.get("/bill/")
def read_bills_route(db: Session = Depends(get_db)):
    """
    Handles the HTTP request to retrieve all bills.

    This route function interacts with the service layer to fetch a list of bills
    from the database. It uses dependency injection to obtain a database session.

    Args:
        db (Session): A SQLAlchemy database session provided by the `get_db` dependency.

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
        db (Session, optional): The database session dependency. Defaults to the session provided by `get_db`.

    Returns:
        Any: The result of the `delete_bill_serv` service function, which handles the deletion logic.
    """
    return delete_bill_serv(bill_id, db)

# Endpoint to update a specific bill by its ID
@router.put("/bill/{bill_id}")
def update_bill_route(bill_id: int, bill_update: BillCreate, db: Session = Depends(get_db)):
    """
    Updates an existing bill with the provided details.

    Args:
        bill_id (int): The unique identifier of the bill to be updated.
        bill_update (BillCreate): An object containing the updated details of the bill.
        db (Session, optional): The database session dependency. Defaults to the result of `Depends(get_db)`.

    Returns:
        The updated bill object or the result of the `update_bill_serv` service function.
    """
    return update_bill_serv(bill_id, bill_update, db)