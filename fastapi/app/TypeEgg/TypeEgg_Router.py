from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.TypeEgg.TypeEgg_Schema import *
from app.TypeEgg.TypeEgg_Service import *

router = APIRouter()

# Endpoint to create a new typeEgg
# Accepts a TypeEggCreate object and returns a TypeEggResponse with the created typeEgg
@router.post("/typeEgg/", status_code=201, response_model=TypeEggResponse)
def create_typeEgg_route(typeEgg: TypeEggCreate, db: Session = Depends(get_db)):
    return create_typeEgg_serv(typeEgg, db)

# Endpoint to get a specific typeEgg by its ID
# Returns the typeEgg matching the provided ID
@router.get("/typeEgg/{typeEgg_id}", response_model=TypeEggResponse)
def get_typeEgg_route(typeEgg_id: int, db: Session = Depends(get_db)):
    return read_typeEgg_serv(typeEgg_id, db)

# Endpoint to get a list of all typeEggs
# Returns a list of typeEggs
@router.get("/typeEggs/", response_model=list[TypeEggResponse])
def get_typeEggs_route(db: Session = Depends(get_db)):
    return read_typeEggs_serv(db)

# Endpoint to update a typeEgg's information by its ID
# Accepts a TypeEggCreate object with the updated data
@router.put("/typeEgg/{typeEgg_id}", response_model=TypeEggResponse)
def update_typeEgg_route(typeEgg_id: int, typeEgg_update: TypeEggCreate, db: Session = Depends(get_db)):
    return update_typeEgg_serv(typeEgg_id, typeEgg_update, db)

# Endpoint to delete a typeEgg by its ID
# Returns a success message once the typeEgg is deleted
@router.delete("/typeEgg/{typeEgg_id}")
def delete_typeEgg_route(typeEgg_id: int, db: Session = Depends(get_db)):
    return delete_typeEgg_serv(typeEgg_id, db)
