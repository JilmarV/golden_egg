"""Repository functions for managing TypeEggs in the database."""

from sqlalchemy.orm import Session
from app.TypeEgg.typeegg_model import TypeEgg
from app.TypeEgg.typeegg_schema import TypeEggCreate
from app.db.session import get_db

from fastapi import Depends, HTTPException


def create_typeegg(typeegg: TypeEggCreate, db: Session):
    """Creates a new TypeEgg in the database."""
    db_typeegg = TypeEgg(**typeegg.model_dump())
    db.add(db_typeegg)
    db.commit()
    db.refresh(db_typeegg)
    return db_typeegg


def read_typeeggs(db: Session = Depends(get_db)):
    """Retrieves all TypeEggs from the database."""
    return db.query(TypeEgg).all()


def read_typeegg(typeegg_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific TypeEgg by its ID."""
    typeegg = db.query(TypeEgg).filter(TypeEgg.id == typeegg_id).first()
    if typeegg is None:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    return typeegg


def update_typeegg(
    typeegg_id: int, typeegg_update: TypeEggCreate, db: Session = Depends(get_db)
):
    """Updates an existing TypeEgg in the database by its ID."""
    typeegg = db.query(TypeEgg).filter(TypeEgg.id == typeegg_id).first()
    if typeegg is None:
        raise HTTPException(status_code=404, detail="TypeEgg not found")

    for key, value in typeegg_update.model_dump(exclude_unset=True).items():
        setattr(typeegg, key, value)

    db.commit()
    db.refresh(typeegg)
    return typeegg


def delete_typeegg(typeegg_id: int, db: Session = Depends(get_db)):
    """Deletes a TypeEgg from the database by its ID."""
    typeegg = db.query(TypeEgg).filter(TypeEgg.id == typeegg_id).first()
    if typeegg is None:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    db.delete(typeegg)
    db.commit()
    return {"message": "TypeEgg deleted successfully"}
