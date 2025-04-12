# app/api/v1/egg_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.egg import EggCreate, EggResponse
from app.services.egg_service import create_egg, get_egg

router = APIRouter()

@router.post("/", response_model=EggResponse)
def create_egg_route(egg: EggCreate, db: Session = Depends(get_db)):
    return create_egg(db, egg)

@router.get("/{egg_id}", response_model=EggResponse)
def get_egg_route(egg_id: int, db: Session = Depends(get_db)):
    return get_egg(db, egg_id)
