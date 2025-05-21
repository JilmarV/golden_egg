"""Router for handling role-related API endpoints."""

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.Role.role_schema import RoleCreate, RoleResponse
from app.Role.role_service import (
    create_role_serv,
    read_role_serv,
    read_roles_serv,
    update_role_serv,
    delete_role_serv,
)

from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/", status_code=201, response_model=RoleResponse)
def create_role_route(role: RoleCreate, db: Session = Depends(get_db)):
    """
    Creates a new role in the database.

    Args:
        role (RoleCreate): The data required to create a new role.
        db (Session, optional): The database session dependency.

    Returns:
        Role: The created role object.

    Raises:
        HTTPException: If the role could not be created.
    """
    return create_role_serv(role, db)


@router.get("/{role_id}", response_model=RoleResponse)
def get_role_route(role_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a role by its unique identifier.

    Args:
        role_id (int): The unique identifier of the role to retrieve.
        db (Session, optional): SQLAlchemy database session dependency.

    Returns:
        Role: The role object corresponding to the provided ID.

    Raises:
        HTTPException: If the role with the specified ID does not exist.
    """
    return read_role_serv(role_id, db)


@router.get("/", response_model=list[RoleResponse])
def get_roles_route(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all roles from the database.

    Args:
        db (Session, optional): SQLAlchemy database session dependency.
        Defaults to Depends(get_db).

    Returns:
        List[Role]: A list of role objects retrieved from the database.
    """
    return read_roles_serv(db)


@router.put("/{role_id}", response_model=RoleResponse)
def update_role_route(
    role_id: int, role_update: RoleCreate, db: Session = Depends(get_db)
):
    """
    Updates an existing role by its ID.

    Args:
        role_id (int): The unique identifier of the role to update.
        role_update (RoleCreate): The data to update the role with.
        db (Session, optional): The database session dependency.

    Returns:
        The updated role object.

    Raises:
        HTTPException: If the role with the given ID does not exist.
    """
    return update_role_serv(role_id, role_update, db)


@router.delete("/{role_id}", response_model=dict)
def delete_role_route(role_id: int, db: Session = Depends(get_db)):
    """
    Deletes a role from the database by its ID.

    Args:
        role_id (int): The unique identifier of the role to be deleted.
        db (Session, optional): SQLAlchemy database session dependency.
        Defaults to Depends(get_db).

    Returns:
        Any: The result of the delete operation, typically a confirmation message or status.
    """
    return delete_role_serv(role_id, db)
