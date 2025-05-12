from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.Egg.Egg_Model import *
from app.Egg.Egg_Schema import *
from app.Egg.Egg_Repository import *
from fastapi.app.Supplier.supplier_model import *
from app.TypeEgg.TypeEgg_Model import *

# Service to create a new egg
def create_egg_service(egg: EggCreate, db: Session):
    if not egg.color.strip():
        raise HTTPException(status_code=400, detail="Color is required")
    if egg.buy_price <= 0:
        raise HTTPException(status_code=400, detail="Buy price must be greater than 0")
    if egg.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    if egg.expiration_date <= date.today():
        raise HTTPException(status_code=400, detail="Expiration date must be in the future")
    supplier = db.query(Supplier).filter(Supplier.id == egg.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    type_egg = db.query(TypeEgg).filter(TypeEgg.id == egg.type_id).first()
    if not type_egg:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    return create_egg(egg, db)

# Service to retrieve all eggs
def get_all_eggs_service(db: Session):
    return get_all_eggs(db)

# Service to retrieve an egg by its ID
def get_egg_by_id_service(egg_id: int, db: Session):
    egg = get_egg_by_id(egg_id, db)
    if not egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    return egg

# Service to update an existing egg
def update_egg_service(egg_id: int, egg: EggCreate, db: Session):
    existing_egg = get_egg_by_id(egg_id, db)
    if not existing_egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    if not egg.color.strip():
        raise HTTPException(status_code=400, detail="Color is required")
    if egg.buy_price <= 0:
        raise HTTPException(status_code=400, detail="Buy price must be greater than 0")
    if egg.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    if egg.expiration_date <= date.today():
        raise HTTPException(status_code=400, detail="Expiration date must be in the future")
    supplier = db.query(Supplier).filter(Supplier.id == egg.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    type_egg = db.query(TypeEgg).filter(TypeEgg.id == egg.type_id).first()
    if not type_egg:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    return update_egg(egg_id, egg, db)

# Service to delete an egg
def delete_egg_service(egg_id: int, db: Session):
    egg = get_egg_by_id(egg_id, db)
    if not egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    return delete_egg(egg_id, db)
