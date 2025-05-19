"""Service layer for user-related operations."""

# pylint: disable=import-error, no-name-in-module

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.session import get_db
from app.User.user_schema import UserCreate
from app.Role.role_model import Role
from app.User.user_repository import (
    read_users,
    read_user,
    create_user,
    delete_user,
    update_user,
    read_users_by_role,
    check_previous_user
)

def read_users_serv(db: Session):
    """Service to get all users."""
    return read_users(db)


def read_user_serv(user_id: int, db: Session):
    """Service to get a user by ID."""
    return read_user(user_id, db)


def create_user_serv(user: UserCreate, db: Session):
    """Service to create a new user."""
    for attr in ["email", "username", "address"]:
        if check_previous_user(db, attr, getattr(user, attr)):
            raise HTTPException(status_code=400, detail=f"{attr.capitalize()} Usuario con especificaciones ya existe")
    if not user.role_ids:
        raise HTTPException(status_code=400, detail="El usuario debe tener al menos un rol")
    roles = db.query(Role).filter(Role.id.in_(user.role_ids)).all()
    if len(roles) != len(set(user.role_ids)):
        raise HTTPException(status_code=400, detail="Uno o más roles no existen")
    return create_user(user, roles, db)


def delete_user_serv(user_id: int, db: Session):
    """Service to delete a user by ID."""
    return delete_user(user_id, db)


def update_user_serv(user_id: int, user_update: UserCreate, db: Session):
    """Service to update a user by ID."""
    return update_user(user_id, user_update, db)

def read_users_by_role_serv(role_id: int, db: Session):
    return read_users_by_role(role_id, db)