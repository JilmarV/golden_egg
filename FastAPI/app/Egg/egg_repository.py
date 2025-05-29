"""Repository module for Egg operations."""

from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.db.session import get_db
from app.Egg.egg_model import Egg
from app.Egg.egg_schema import EggCreate, EggSummaryDto
from app.TypeEgg.typeegg_model import TypeEgg


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


# Search for eggs in stock by type egg ID
def search_eggs_stock(type_egg_id: int, db: Session):
    """Search for eggs in stock by type egg ID.
    Args:
        type_egg_id (int): The ID of the type egg to search for.
        db (Session): The database session.
    Returns:
        list[Egg]: A list of eggs that match the type egg ID.
    """
    return db.query(Egg).filter(Egg.type_egg_id == type_egg_id).all()


# Retrieves the total available quantity of eggs (SUM)
def get_total_egg_quantity(db: Session):
    """
    Get the total quantity of eggs in the database.

    Args:
        db (Session): The database session.

    Returns:
        int: The total quantity of available eggs.
    """
    total_quantity = db.query(func.sum(Egg.availableQuantity)).scalar()
    return total_quantity


# Retrieves summarized data of eggs grouped by type and color
def get_egg_summaries(db: Session):
    """
    Retrieve summarized data of eggs grouped by type and color.
    Returns max sellPrice and expirationDate for each group.
    """
    results = db.query(
        Egg.type_egg_id,
        Egg.color,
        func.max(Egg.sellPrice),
        func.max(Egg.expirationDate)
    ).group_by(Egg.type_egg_id, Egg.color).all()

    summaries = []
    for type_id, color, max_price, max_exp in results:
        type_egg = db.query(TypeEgg).filter(TypeEgg.id == type_id).first()
        summaries.append(
            EggSummaryDto(
                type_egg=type_egg,
                color=color,
                sellPrice=max_price,
                expirationDate=max_exp
            )
        )
    return summaries


# Retrieves eggs filtered by color and type, ordered by expiration
def find_eggs_by_color_and_type(color: str, type_egg_id: int, db: Session):
    """
    Retrieve eggs filtered by color and type, ordered by expirationDate.
    
    Args:
        color (str): The color of the egg.
        type_egg_id (int): The ID of the egg type.
        db (Session): The database session.
    
    Returns:
        list[Egg]: Filtered list of eggs.
    """
    return db.query(Egg).filter(
        Egg.color == color,
        Egg.type_egg_id == type_egg_id
    ).order_by(Egg.expirationDate.asc()).all()
