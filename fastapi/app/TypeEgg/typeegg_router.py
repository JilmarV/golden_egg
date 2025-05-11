"""Router for TypeEgg endpoints in the FastAPI application."""

# pylint: disable=import-error, no-name-in-module

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.TypeEgg.typeegg_schema import TypeEggCreate, TypeEggResponse
from app.TypeEgg.typeegg_service import (
    create_typeegg_service,
    read_typeegg_service,
    read_typeeggs_service,
    update_typeegg_service,
    delete_typeegg_service,
)

from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/typeeggs/", status_code=201, response_model=TypeEggResponse)
def create_typeegg(typeegg: TypeEggCreate, db: Session = Depends(get_db)):
    """Creates a new TypeEgg."""
    return create_typeegg_service(typeegg, db)


@router.get("/typeeggs/{typeegg_id}", response_model=TypeEggResponse)
def get_typeegg(typeegg_id: int, db: Session = Depends(get_db)):
    """Retrieves a TypeEgg by its ID."""
    return read_typeegg_service(typeegg_id, db)


@router.get("/typeeggs/", response_model=list[TypeEggResponse])
def get_typeeggs(db: Session = Depends(get_db)):
    """Retrieves all TypeEggs."""
    return read_typeeggs_service(db)


@router.put("/typeeggs/{typeegg_id}", response_model=TypeEggResponse)
def update_typeegg(
    typeegg_id: int,
    typeegg_update: TypeEggCreate,
    db: Session = Depends(get_db),
):
    """Updates an existing TypeEgg by ID."""
    return update_typeegg_service(typeegg_id, typeegg_update, db)


@router.delete("/typeeggs/{typeegg_id}")
def delete_typeegg(typeegg_id: int, db: Session = Depends(get_db)):
    """Deletes a TypeEgg by ID."""
    return delete_typeegg_service(typeegg_id, db)
