from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from app.WebVisit.WebVisit_Service import save_visit_service, get_visit_count_service
from app.WebVisit.WebVisit_Schema import WebVisitResponse

router = APIRouter()

# Endpoint to register a web visit
@router.post("/visit", response_model=WebVisitResponse)
def register_visit(request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host
    return save_visit_service(client_ip, db)

# Endpoint to get the total visit count
@router.get("/visit/count")
def visit_count(db: Session = Depends(get_db)):
    return {"count": get_visit_count_service(db)}
