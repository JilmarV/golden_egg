"""Router for handling role-related API endpoints."""

from sqlalchemy.orm import Session

from FastAPI.app.db.session import get_db
from FastAPI.app.Role.role_schema import RoleCreate, RoleResponse
from FastAPI.app.Role.role_service import (
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
    """Creates a new role."""
    return create_role_serv(role, db)


@router.get("/{role_id}", response_model=RoleResponse)
def get_role_route(role_id: int, db: Session = Depends(get_db)):
    """Retrieves a role by ID."""
    return read_role_serv(role_id, db)


@router.get("/", response_model=list[RoleResponse])
def get_roles_route(db: Session = Depends(get_db)):
    """Retrieves all roles."""
    return read_roles_serv(db)


@router.put("/{role_id}", response_model=RoleResponse)
def update_role_route(
    role_id: int, role_update: RoleCreate, db: Session = Depends(get_db)
):
    """Updates a role by ID."""
    return update_role_serv(role_id, role_update, db)


@router.delete("/{role_id}", response_model=dict)
def delete_role_route(role_id: int, db: Session = Depends(get_db)):
    """Deletes a role by ID."""
    return delete_role_serv(role_id, db)
