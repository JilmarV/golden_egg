"""Router module for Egg endpoints."""

# pylint: disable=import-error, no-name-in-module

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.Egg.egg_service import (
    create_egg_service,
    get_egg_by_id_service,
    delete_egg_service,
    get_all_eggs_service,
    update_egg_service,
    get_eggs_stock_service,
    get_total_egg_quantity_serv,
)
from app.Egg.egg_schema import EggCreate, EggResponse
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/", status_code=201, response_model=EggResponse)
def create_egg_route(egg: EggCreate, db: Session = Depends(get_db)):
    """
    Handles the creation of a new egg resource.

    Args:
        egg (EggCreate): The data required to create a new egg, provided as an
        instance of the EggCreate schema.
        db (Session): The database session dependency, automatically injected
        by FastAPI.

    Returns:
        The result of the egg creation process, as returned by the
        create_egg_service function.
    """
    return create_egg_service(egg, db)


@router.get("/{egg_id}", response_model=EggResponse)
def get_egg_by_id_route(egg_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an egg by its unique identifier.

    Args:
        egg_id (int): The unique identifier of the egg to retrieve.
        db (Session, optional): The database session dependency.
        Defaults to the result of `Depends(get_db)`.

    Returns:
        The egg object retrieved by its ID, as returned by the
        `get_egg_by_id_service` function.
    """
    return get_egg_by_id_service(egg_id, db)


@router.delete("/{egg_id}", response_model=dict)
def delete_egg_route(egg_id: int, db: Session = Depends(get_db)):
    """
    Deletes an egg record from the database.

    Args:
        egg_id (int): The unique identifier of the egg to be deleted.
        db (Session, optional): The database session dependency.
        Defaults to the session provided by `get_db`.

    Returns:
        Any: The result of the `delete_egg_service` function,
        which handles the deletion logic.
    """
    return delete_egg_service(egg_id, db)


@router.get("/", response_model=list[EggResponse])
def get_all_eggs_route(db: Session = Depends(get_db)):
    """
    Handles the HTTP GET request to retrieve all eggs.

    Args:
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        List[Egg]: A list of all egg records retrieved from the database.
    """
    return get_all_eggs_service(db)


@router.put("/{egg_id}", response_model=EggResponse)
def update_egg_route(egg_id: int, egg_update: EggCreate, db: Session = Depends(get_db)):
    """
    Updates the details of an existing egg in the database.

    Args:
        egg_id (int): The unique identifier of the egg to be updated.
        egg_update (EggCreate): An object containing the updated details of the egg.
        db (Session): The database session dependency.

    Returns:
        The updated egg object or the result of the update operation.
    """
    return update_egg_service(egg_id, egg_update, db)


@router.get("/stock/{type_egg_id}", response_model=EggResponse)
def get_eggs_stock(type_egg_id: int, db: Session = Depends(get_db)):
    """Retrieves the stock of eggs by type.
    Args:
        type_egg_id (int): The unique identifier of the egg type.
        db (Session): The database session dependency.
    Returns:
        EggResponse: The stock of eggs for the specified type.
    """
    return get_eggs_stock_service(type_egg_id, db)

@router.get("/search/count_this_month", response_model = int)
def get_total_egg_quantity_route(db: Session = Depends(get_db)):
    """
    Retrieves the total quantity of eggs in the database.

    Args:
        db (Session): The database session dependency.

    Returns:
        int: The total quantity of eggs in the database.
    """
    return get_total_egg_quantity_serv(db)
