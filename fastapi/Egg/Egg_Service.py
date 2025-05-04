from sqlalchemy.orm import Session
from fastapi import HTTPException
from Egg.Egg_Model import *
from Egg.Egg_Schema import *
from Egg.Egg_Repository import *
from Supplier.Supplier_Model import *
from Inventory.Inventory_Model import *

#Service to create a new egg
def create_egg_service(egg: EggCreate, db: Session):
    # Validar existencia de proveedor
    supplier = db.query(Supplier).filter(Supplier.id == egg.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    # Validar existencia de inventario
    inventory = db.query(Inventory).filter(Inventory.id == egg.inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return create_egg(egg, db)

# Service to retrieve all eggs
def get_all_eggs_service(db: Session):
    return get_all_eggs(db)

# Service to retrieve an egg by its ID
def get_egg_by_id_service(egg_id: int, db: Session):
    return get_egg_by_id(egg_id, db)

# Service to update an existing egg
def update_egg_service(egg_id: int, egg: EggCreate, db: Session):
    # Verify that the egg exists
    existing_egg = get_egg_by_id(egg_id, db)
    if not existing_egg:
        raise HTTPException(status_code=404, detail="Egg not found")

    # Verificar que el nuevo proveedor existe
    supplier = db.query(Supplier).filter(Supplier.id == egg.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    # Verificar que el nuevo inventario existe
    inventory = db.query(Inventory).filter(Inventory.id == egg.inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return update_egg(egg_id, egg, db)

# Service to delete an egg
def delete_egg_service(egg_id: int, db: Session):
    return delete_egg(egg_id, db)
