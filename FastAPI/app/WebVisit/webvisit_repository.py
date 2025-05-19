"""Repository functions for managing web visit data."""

from sqlalchemy.orm import Session
from app.WebVisit.webvisit_model import WebVisit


def save_visit(ip: str, db: Session):
    """Saves a new web visit with the given IP address."""
    visit = WebVisit(ip=ip)
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


def get_visit_count(db: Session):
    """Returns the total number of web visits recorded."""
    return db.query(WebVisit).count()
