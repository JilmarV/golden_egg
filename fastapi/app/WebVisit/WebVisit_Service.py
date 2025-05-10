from sqlalchemy.orm import Session
from app.WebVisit.WebVisit_Repository import save_visit, get_visit_count

# Save a visit using the request's IP
def save_visit_service(ip: str, db: Session):
    return save_visit(ip, db)

# Return total number of visits
def get_visit_count_service(db: Session):
    return get_visit_count(db)
