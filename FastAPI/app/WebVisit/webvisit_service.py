"""Service layer for handling web visit operations."""

from sqlalchemy.orm import Session
from app.WebVisit.webvisit_repository import save_visit, get_visit_count


def save_visit_service(ip: str, db: Session):
    """Service to save a new web visit using the client's IP address."""
    return save_visit(ip, db)


def get_visit_count_service(db: Session):
    """Service to retrieve the total number of recorded web visits."""
    return get_visit_count(db)
