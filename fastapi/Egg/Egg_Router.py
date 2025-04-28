from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from Egg.Egg_Model import *
from Egg.Egg_Schema import *
from Egg.Egg_Service import *

router = APIRouter()

# Endpoint to create a new egg
# Accepts an EggCreate object and returns an EggResponse with the created egg
@router.post("/egg/", status_code=201, response_model=EggResponse)
def create_egg_route(egg: EggCreate, db: Session = Depends(get_db)):
    return create_egg_service(egg, db)

# Endpoint to get a specific egg by its ID
# Returns the egg matching the provided ID
@router.get("/egg/{egg_id}", response_model=EggResponse)
def get_egg_by_id_route(egg_id: int, db: Session = Depends(get_db)):
    return get_egg_by_id_service(egg_id, db)

# Endpoint to delete an egg by its ID
# Returns a success message once the egg is deleted
@router.delete("/egg/{egg_id}", response_model=dict)
def delete_egg_route(egg_id: int, db: Session = Depends(get_db)):
    return delete_egg_service(egg_id, db)

# Endpoint to get a list of all eggs
# Returns a list of eggs
@router.get("/egg/", response_model=list[EggResponse])
def get_all_eggs_route(db: Session = Depends(get_db)):
    return get_all_eggs_service(db)

# Endpoint to update an egg's information by its ID
# Accepts an EggCreate object with the updated data
@router.put("/egg/{egg_id}", response_model=EggResponse)
def update_egg_route(egg_id: int, egg_update: EggCreate, db: Session = Depends(get_db)):
    return update_egg_service(egg_id, egg_update, db)
