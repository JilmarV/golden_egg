from sqlalchemy.orm import Session
from fastapi import HTTPException
from TypeEgg.TypeEgg_Model import TypeEgg
from TypeEgg.TypeEgg_Schema import TypeEggCreate
from TypeEgg import TypeEgg_Repository as repo

# Service to create a new TypeEgg
def create_type_egg_serv(type_egg: TypeEggCreate, db: Session):
    return repo.create_type_egg(type_egg, db)

# Service to get all TypeEgg records
def read_type_eggs_serv(db: Session):
    return repo.read_type_eggs(db)

# Service to get a TypeEgg by ID
def read_type_egg_serv(type_egg_id: int, db: Session):
    return repo.read_type_egg(type_egg_id, db)

# Service to update a TypeEgg by ID
def update_type_egg_serv(type_egg_id: int, type_egg_update: TypeEggCreate, db: Session):
    return repo.update_type_egg(type_egg_id, type_egg_update, db)

# Service to delete a TypeEgg by ID
def delete_type_egg_serv(type_egg_id: int, db: Session):
    return repo.delete_type_egg(type_egg_id, db)
