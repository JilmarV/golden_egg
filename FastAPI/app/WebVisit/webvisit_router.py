"""Router for tracking and retrieving web visit data."""

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.WebVisit.webvisit_service import (
    save_visit_service,
    get_visit_count_service,
)
from app.WebVisit.webvisit_schema import WebVisitResponse

from fastapi import APIRouter, Request, Depends

router = APIRouter()


@router.post("/", response_model=WebVisitResponse)
def register_visit(request: Request, db: Session = Depends(get_db)):
    """
    Registers a web visit by extracting the client's IP address from
    the request and saving the visit information to the database.

    Args:
        request (Request): The incoming HTTP request object.
        db (Session, optional): SQLAlchemy database session,
        injected by FastAPI dependency.

    Returns:
        Any: The result of the save_visit_service function,
        which handles persisting the visit information.
    """
    client_ip = request.client.host
    return save_visit_service(client_ip, db)


@router.get("/count")
def visit_count(db: Session = Depends(get_db)):
    """
    Retrieve the total number of visits from the database.

    Args:
        db (Session, optional): SQLAlchemy database session dependency.
        Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the total visit count with the key 'count'.
    """
    return {"count": get_visit_count_service(db)}
