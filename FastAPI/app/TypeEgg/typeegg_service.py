"""Service layer for TypeEgg operations."""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import Depends
from app.TypeEgg.typeegg_repository import (
    create_typeegg,
    read_typeegg,
    read_typeeggs,
    update_typeegg,
    delete_typeegg,
    get_db,
)
from app.TypeEgg.typeegg_schema import TypeEggCreate


def create_typeegg_service(typeegg: TypeEggCreate, db: Session = Depends(get_db)):
    """Creates a new TypeEgg using the repository."""
    if not typeegg.name.strip():
        raise HTTPException(status_code=400, detail="name is required")
    return create_typeegg(typeegg, db)


def read_typeegg_service(typeegg_id: int, db: Session = Depends(get_db)):
    """Retrieves a TypeEgg by its ID."""
    return read_typeegg(typeegg_id, db)


def read_typeeggs_service(db: Session = Depends(get_db)):
    """Retrieves all TypeEggs."""
    return read_typeeggs(db)


def update_typeegg_service(
    typeegg_id: int,
    typeegg_update: TypeEggCreate,
    db: Session = Depends(get_db),
):
    """Updates an existing TypeEgg by ID."""
    if not typeegg_update.name.strip():
        raise HTTPException(status_code=400, detail="name is required")
    return update_typeegg(typeegg_id, typeegg_update, db)


def delete_typeegg_service(typeegg_id: int, db: Session = Depends(get_db)):
    """Deletes a TypeEgg by ID."""
    return delete_typeegg(typeegg_id, db)
