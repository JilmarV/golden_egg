"""Router for tracking and retrieving web visit data."""

# pylint: disable=import-error, no-name-in-module

from sqlalchemy.orm import Session

from db.session import get_db
from fastapi.app.WebVisit.webvisit_service import save_visit_service, get_visit_count_service
from fastapi.app.WebVisit.webvisit_schema import WebVisitResponse

from fastapi import APIRouter, Request, Depends

router = APIRouter()


@router.post("/visit", response_model=WebVisitResponse)
def register_visit(request: Request, db: Session = Depends(get_db)):
    """Registers a web visit using the client's IP address."""
    client_ip = request.client.host
    return save_visit_service(client_ip, db)


@router.get("/visit/count")
def visit_count(db: Session = Depends(get_db)):
    """Returns the total number of web visits recorded."""
    return {"count": get_visit_count_service(db)}
