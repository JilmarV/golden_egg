"""Service module for Egg operations."""

from datetime import date
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.Egg.egg_schema import EggCreate
from app.Egg.egg_repository import (
    create_egg,
    get_all_eggs,
    get_egg_by_id,
    get_total_egg_quantity,
    update_egg,
    delete_egg,
    search_eggs_stock,
)
from app.Supplier.supplier_model import Supplier
from app.TypeEgg.typeegg_model import TypeEgg


# Service to create a new egg
def create_egg_service(egg: EggCreate, db: Session):
    """Create a new egg in the database."""
    if not egg.color.strip():
        raise HTTPException(status_code=400, detail="Color is required")
    if egg.sellPrice <= 0:
        raise HTTPException(status_code=400, detail="Buy price must be greater than 0")
    if egg.avalibleQuantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    if egg.expirationDate <= date.today():
        raise HTTPException(
            status_code=400, detail="Expiration date must be in the future"
        )
    supplier = db.query(Supplier).filter(Supplier.id == egg.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    type_egg = db.query(TypeEgg).filter(TypeEgg.id == egg.type_egg_id).first()
    if not type_egg:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    return create_egg(egg, db)


# Service to retrieve all eggs
def get_all_eggs_service(db: Session):
    """Retrieve all eggs from the database."""
    return get_all_eggs(db)


# Service to retrieve an egg by its ID
def get_egg_by_id_service(egg_id: int, db: Session):
    """Retrieve an egg by its ID."""
    egg = get_egg_by_id(egg_id, db)
    if not egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    return egg


# Service to update an existing egg
def update_egg_service(egg_id: int, egg: EggCreate, db: Session):
    """Update an existing egg in the database."""
    existing_egg = get_egg_by_id(egg_id, db)
    if not existing_egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    if not egg.color.strip():
        raise HTTPException(status_code=400, detail="Color is required")
    if egg.sellPrice <= 0:
        raise HTTPException(status_code=400, detail="Buy price must be greater than 0")
    if egg.avalibleQuantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    if egg.expirationDate <= date.today():
        raise HTTPException(
            status_code=400, detail="Expiration date must be in the future"
        )
    supplier = db.query(Supplier).filter(Supplier.id == egg.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    type_egg = db.query(TypeEgg).filter(TypeEgg.id == egg.type_egg_id).first()
    if not type_egg:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    return update_egg(egg_id, egg, db)


# Service to delete an egg
def delete_egg_service(egg_id: int, db: Session):
    """Delete an egg from the database."""
    egg = get_egg_by_id(egg_id, db)
    if not egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    return delete_egg(egg_id, db)


def get_eggs_stock_service(type_egg_id: int, db: Session):
    """Get eggs in stock by type egg ID."""
    return search_eggs_stock(type_egg_id, db)


def get_total_egg_quantity_serv(db: Session):
    """Get the total quantity of eggs in stock."""
    count = get_total_egg_quantity(db)
    if not count:
        raise HTTPException(status_code=404, detail="No eggs found")
    return count or 0
