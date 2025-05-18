"""Service layer for role operations."""

from sqlalchemy.orm import Session

from FastAPI.app.db.session import get_db
from FastAPI.app.Role.role_schema import RoleCreate
from FastAPI.app.Role.role_repository import (
    create_role,
    read_role,
    read_roles,
    update_role,
    delete_role,
)

from fastapi import Depends


def create_role_serv(role: RoleCreate, db: Session = Depends(get_db)):
    """Creates a new role."""
    return create_role(role, db)


def read_role_serv(role_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific role by ID."""
    return read_role(role_id, db)


def read_roles_serv(db: Session = Depends(get_db)):
    """Retrieves all roles."""
    return read_roles(db)


def update_role_serv(
    role_id: int, role_update: RoleCreate, db: Session = Depends(get_db)
):
    """Updates an existing role by ID."""
    return update_role(role_id, role_update, db)


def delete_role_serv(role_id: int, db: Session = Depends(get_db)):
    """Deletes a role by ID."""
    return delete_role(role_id, db)
