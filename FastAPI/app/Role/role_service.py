"""Service layer for role operations."""

from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException
from app.db.session import get_db
from app.Role.role_schema import RoleCreate
from app.Role.role_repository import (
    create_role,
    read_role,
    read_roles,
    update_role,
    delete_role,
    check_previous_role,
)


def create_role_serv(role: RoleCreate, db: Session = Depends(get_db)):
    """Creates a new role."""
    for attr in ["name"]:
        if check_previous_role(db, attr, getattr(role, attr)):
            raise HTTPException(
                status_code=400, detail=f"{attr.capitalize()} Role already exists"
            )
    if not role.name.strip():
        raise HTTPException(status_code=400, detail="name is required")
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
    if not role_update.name.strip():
        raise HTTPException(status_code=400, detail="name is required")
    return update_role(role_id, role_update, db)


def delete_role_serv(role_id: int, db: Session = Depends(get_db)):
    """Deletes a role by ID."""
    return delete_role(role_id, db)
