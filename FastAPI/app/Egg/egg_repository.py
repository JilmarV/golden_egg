"""Repository module for Egg operations."""

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.db.session import get_db
from app.Egg.egg_schema import EggCreate
from app.Egg.egg_model import Egg


# Create a new egg in the database
def create_egg(egg: EggCreate, db: Session = Depends(get_db)):
    """Create a new egg record in the database."""
    db_egg = Egg(**egg.model_dump())
    db.add(db_egg)
    db.commit()
    db.refresh(db_egg)
    return db_egg


# Retrieves all eggs from the database
def get_all_eggs(db: Session = Depends(get_db)):
    """Retrieve all egg records from the database."""
    eggs = db.query(Egg).all()
    return eggs


# Retrieves a specific egg by its ID
def get_egg_by_id(egg_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific egg record by its ID."""
    egg = db.query(Egg).filter(Egg.id == egg_id).first()

    if not egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    return egg


# Updates a specific egg in the database
def update_egg(egg_id: int, egg: EggCreate, db: Session = Depends(get_db)):
    """Update a specific egg record by its ID."""
    db_egg = db.query(Egg).filter(Egg.id == egg_id).first()

    if not db_egg:
        raise HTTPException(status_code=404, detail="Egg not found")

    for key, value in egg.model_dump().items():
        setattr(db_egg, key, value)
    db.commit()
    db.refresh(db_egg)
    return db_egg


# Deletes a specific egg from the database
def delete_egg(egg_id: int, db: Session = Depends(get_db)):
    """Delete a specific egg record by its ID."""
    db_egg = db.query(Egg).filter(Egg.id == egg_id).first()

    if not db_egg:
        raise HTTPException(status_code=404, detail="Egg not found")

    db.delete(db_egg)
    db.commit()
    return {"message": "Egg deleted successfully"}


def search_eggs_stock(type_egg_id: int, db: Session):
    """Search for eggs in stock by type egg ID.
    Args:
        type_egg_id (int): The ID of the type egg to search for.
        db (Session): The database session.
    Returns:
        list[Egg]: A list of eggs that match the type egg ID.
    """
    return db.query(Egg).filter(Egg.type_egg_id == type_egg_id).all()


def get_total_egg_quantity(db: Session):
    """
    Get the total quantity of eggs in the database.

    Args:
        db (Session): The database session.

    Returns:
        int: The total quantity of eggs.
    """
    count = db.query(Egg).count()
    return count
