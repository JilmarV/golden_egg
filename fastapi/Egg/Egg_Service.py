from sqlalchemy.orm import Session
from fastapi import HTTPException
from Egg.Egg_Model import *
from Egg.Egg_Schema import *
from Egg.Egg_Repository import *

# Service to create a new egg
def create_egg_service(egg: EggCreate, db: Session):
    return create_egg(egg, db)

# Service to retrieve all eggs
def get_all_eggs_service(db: Session):
    return get_all_eggs(db)

# Service to retrieve an egg by its ID
def get_egg_by_id_service(egg_id: int, db: Session):
    return get_egg_by_id(egg_id, db)

# Service to update an existing egg
def update_egg_service(egg_id: int, egg: EggCreate, db: Session):
    return update_egg(egg_id, egg, db)

# Service to delete an egg
def delete_egg_service(egg_id: int, db: Session):
    return delete_egg(egg_id, db)
