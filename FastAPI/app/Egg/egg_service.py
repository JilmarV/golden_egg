"""Service module for Egg operations."""

from datetime import date
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
    get_egg_summaries,
    find_eggs_by_color_and_type,
)
from app.Supplier.supplier_model import Supplier
from app.TypeEgg.typeegg_model import TypeEgg


# Service to create a new egg
def create_egg_service(egg: EggCreate, db: Session):
    """Create a new egg in the database."""
    _validate_egg(egg, db)
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
    _validate_egg(egg, db)
    return update_egg(egg_id, egg, db)


# Service to delete an egg
def delete_egg_service(egg_id: int, db: Session):
    """Delete an egg from the database."""
    egg = get_egg_by_id(egg_id, db)
    if not egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    return delete_egg(egg_id, db)


# Service to get stock of eggs by type
def get_eggs_stock_service(type_egg_id: int, db: Session):
    """Get eggs in stock by type egg ID."""
    eggs = search_eggs_stock(type_egg_id, db)
    if not eggs:
        raise HTTPException(status_code=404, detail="No eggs found for this type")
    return eggs


# Service to get the total available quantity of eggs
def get_total_egg_quantity_serv(db: Session):
    """Get the total quantity of eggs in stock."""
    total = get_total_egg_quantity(db)
    if total is None:
        raise HTTPException(status_code=404, detail="No eggs found")
    return total


# Service to get summarized egg data grouped by type and color
def get_egg_summaries_service(db: Session):
    """Retrieve summarized data of eggs grouped by type and color."""
    summaries = get_egg_summaries(db)
    if not summaries:
        raise HTTPException(status_code=404, detail="No egg summaries available")
    return summaries


# Service to get eggs filtered by color and type
def find_eggs_by_color_and_type_service(color: str, type_egg_id: int, db: Session):
    """Retrieve eggs filtered by color and type."""
    if not color.strip():
        raise HTTPException(status_code=400, detail="Color must be provided")
    type_egg = db.query(TypeEgg).filter(TypeEgg.id == type_egg_id).first()
    if not type_egg:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    eggs = find_eggs_by_color_and_type(color, type_egg_id, db)
    if not eggs:
        raise HTTPException(status_code=404, detail="No eggs found with this criteria")
    return eggs


# egg field validation
def _validate_egg(egg: EggCreate, db: Session):
    """Validate egg input data."""
    if not egg.color.strip():
        raise HTTPException(status_code=400, detail="Color is required")
    if egg.sellPrice <= 0:
        raise HTTPException(status_code=400, detail="Sell price must be greater than 0")
    if egg.entryPrice <= 0:
        raise HTTPException(status_code=400, detail="Entry price must be greater than 0")
    if egg.availableQuantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    if egg.expirationDate <= date.today():
        raise HTTPException(status_code=400, detail="Expiration date must be in the future")
    supplier = db.query(Supplier).filter(Supplier.id == egg.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    type_egg = db.query(TypeEgg).filter(TypeEgg.id == egg.type_egg_id).first()
    if not type_egg:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
