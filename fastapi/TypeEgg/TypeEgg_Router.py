from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from TypeEgg.TypeEgg_Schema import TypeEggCreate, TypeEggResponse
from TypeEgg.TypeEgg_Service import *

router = APIRouter()

# Endpoint to create a new TypeEgg
# Accepts a TypeEggCreate object and returns the created TypeEggResponse
@router.post("/type-egg/", status_code=201, response_model=TypeEggResponse)
def create_type_egg_route(type_egg: TypeEggCreate, db: Session = Depends(get_db)):
    return create_type_egg_serv(type_egg, db)

# Endpoint to get a specific TypeEgg by ID
# Returns the TypeEgg matching the provided ID
@router.get("/type-egg/{type_egg_id}", response_model=TypeEggResponse)
def get_type_egg_route(type_egg_id: int, db: Session = Depends(get_db)):
    return read_type_egg_serv(type_egg_id, db)

# Endpoint to delete a TypeEgg by ID
# Returns a success message once the TypeEgg is deleted
@router.delete("/type-egg/{type_egg_id}")
def delete_type_egg_route(type_egg_id: int, db: Session = Depends(get_db)):
    return delete_type_egg_serv(type_egg_id, db)

# Endpoint to get a list of all TypeEgg records
# Returns a list of TypeEggResponse
@router.get("/type-egg/", response_model=list[TypeEggResponse])
def read_type_eggs_route(db: Session = Depends(get_db)):
    return read_type_eggs_serv(db)

# Endpoint to update a TypeEgg's information by ID
# Accepts a TypeEggCreate object with the updated data
@router.put("/type-egg/{type_egg_id}", response_model=TypeEggResponse)
def update_type_egg_route(type_egg_id: int, type_egg_update: TypeEggCreate, db: Session = Depends(get_db)):
    return update_type_egg_serv(type_egg_id, type_egg_update, db)
