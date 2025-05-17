"""Service layer for TypeEgg operations."""

# pylint: disable=import-error, no-name-in-module

from sqlalchemy.orm import Session

from app.TypeEgg.typeegg_repository import (
    create_typeegg,
    read_typeegg,
    read_typeeggs,
    update_typeegg,
    delete_typeegg,
    get_db,
)
from app.TypeEgg.typeegg_schema import TypeEggCreate

from fastapi import Depends


def create_typeegg_service(typeegg: TypeEggCreate, db: Session = Depends(get_db)):
    """Creates a new TypeEgg using the repository."""
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
    return update_typeegg(typeegg_id, typeegg_update, db)


def delete_typeegg_service(typeegg_id: int, db: Session = Depends(get_db)):
    """Deletes a TypeEgg by ID."""
    return delete_typeegg(typeegg_id, db)
