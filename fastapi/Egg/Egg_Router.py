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
    """
    Handles the creation of a new egg resource.

    This function acts as a FastAPI route handler for creating a new egg. It
    receives the egg data from the request body, validates it against the
    `EggCreate` schema, and passes it to the service layer for processing.

    Args:
        egg (EggCreate): The data required to create a new egg, validated by the `EggCreate` schema.
        db (Session, optional): The database session dependency, automatically injected by FastAPI.

    Returns:
        The result of the `create_egg_service` function, which typically includes the created egg's details.
    """
    return create_egg_service(egg, db)

# Endpoint to get a specific egg by its ID
# Returns the egg matching the provided ID
@router.get("/egg/{egg_id}", response_model=EggResponse)
def get_egg_by_id_route(egg_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an egg by its unique identifier.

    Args:
        egg_id (int): The unique identifier of the egg to retrieve.
        db (Session, optional): The database session dependency. Defaults to the session provided by `get_db`.

    Returns:
        The egg object retrieved by the service layer, or an appropriate response if the egg is not found.
    """
    return get_egg_by_id_service(egg_id, db)

# Endpoint to delete an egg by its ID
# Returns a success message once the egg is deleted
@router.delete("/egg/{egg_id}", response_model=dict)
def delete_egg_route(egg_id: int, db: Session = Depends(get_db)):
    """
    Deletes an egg record from the database.

    Args:
        egg_id (int): The unique identifier of the egg to be deleted.
        db (Session, optional): The database session dependency. Defaults to the session provided by `get_db`.

    Returns:
        Any: The result of the `delete_egg_service` function, which handles the deletion logic.
    """
    return delete_egg_service(egg_id, db)

# Endpoint to get a list of all eggs
# Returns a list of eggs
@router.get("/egg/", response_model=list[EggResponse])
def get_all_eggs_route(db: Session = Depends(get_db)):
    """
    Handles the HTTP request to retrieve all eggs from the database.

    This route function uses dependency injection to obtain a database session
    and calls the service layer to fetch all egg records.

    Args:
        db (Session): A SQLAlchemy database session provided by the `Depends` function.

    Returns:
        List[Egg]: A list of all egg objects retrieved from the database.
    """
    return get_all_eggs_service(db)

# Endpoint to update an egg's information by its ID
# Accepts an EggCreate object with the updated data
@router.put("/egg/{egg_id}", response_model=EggResponse)
def update_egg_route(egg_id: int, egg_update: EggCreate, db: Session = Depends(get_db)):
    """
    Updates an existing egg record in the database.

    Args:
        egg_id (int): The unique identifier of the egg to be updated.
        egg_update (EggCreate): An object containing the updated data for the egg.
        db (Session, optional): The database session dependency. Defaults to the result of `Depends(get_db)`.

    Returns:
        The updated egg record as returned by the `update_egg_service` function.
    """
    return update_egg_service(egg_id, egg_update, db)
