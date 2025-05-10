from sqlalchemy.orm import Session
from WebVisit.WebVisit_Model import WebVisit

# Save a web visit
def save_visit(ip: str, db: Session):
    visit = WebVisit(ip=ip)
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit

# Get the total count of visits
def get_visit_count(db: Session):
    return db.query(WebVisit).count()
