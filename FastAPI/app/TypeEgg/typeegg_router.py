"""Router for TypeEgg endpoints in the FastAPI application."""

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.TypeEgg.typeegg_schema import TypeEggCreate, TypeEggResponse
from app.TypeEgg.typeegg_service import (
    create_typeegg_service,
    read_typeegg_service,
    read_typeeggs_service,
    update_typeegg_service,
    delete_typeegg_service,
)

from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/", status_code=201, response_model=TypeEggResponse)
def create_typeegg(typeegg: TypeEggCreate, db: Session = Depends(get_db)):
    """
    Creates a new TypeEgg entry in the database.

    Args:
        typeegg (TypeEggCreate): The data required to create a new TypeEgg.
        db (Session, optional): SQLAlchemy database session dependency.

    Returns:
        The created TypeEgg object or the result from the create_typeegg_service function.
    """
    return create_typeegg_service(typeegg, db)


@router.get("/{typeegg_id}", response_model=TypeEggResponse)
def get_typeegg(typeegg_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a TypeEgg record by its ID.

    Args:
        typeegg_id (int): The unique identifier of the TypeEgg to retrieve.
        db (Session, optional): SQLAlchemy database session dependency.

    Returns:
        TypeEgg: The TypeEgg record corresponding to the provided ID, or None if not found.
    """
    return read_typeegg_service(typeegg_id, db)


@router.get("/", response_model=list[TypeEggResponse])
def get_typeeggs(db: Session = Depends(get_db)):
    """
    Retrieve all TypeEgg records from the database.

    Args:
        db (Session, optional): SQLAlchemy database session.
        Automatically provided by FastAPI dependency injection.

    Returns:
        List[TypeEgg]: A list of TypeEgg objects retrieved from the database.
    """
    return read_typeeggs_service(db)


@router.put("/{typeegg_id}", response_model=TypeEggResponse)
def update_typeegg(
    typeegg_id: int,
    typeegg_update: TypeEggCreate,
    db: Session = Depends(get_db),
):
    """
    Update an existing TypeEgg entry in the database.

    Args:
        typeegg_id (int): The unique identifier of the TypeEgg to update.
        typeegg_update (TypeEggCreate): The data to update the TypeEgg with.
        db (Session, optional): SQLAlchemy database session dependency.

    Returns:
        The updated TypeEgg object or the result of the update operation.

    Raises:
        HTTPException: If the TypeEgg with the given ID does not exist or update fails.
    """
    return update_typeegg_service(typeegg_id, typeegg_update, db)


@router.delete("/{typeegg_id}")
def delete_typeegg(typeegg_id: int, db: Session = Depends(get_db)):
    """
    Deletes a TypeEgg record from the database by its ID.

    Args:
        typeegg_id (int): The unique identifier of the TypeEgg to be deleted.
        db (Session, optional): SQLAlchemy database session dependency.

    Returns:
        Any: The result of the delete operation, as returned by the delete_typeegg_service function.
    """
    return delete_typeegg_service(typeegg_id, db)
