"""Service layer for user-related operations."""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.User.user_schema import UserCreate
from app.Auth.auth_service import get_password_hash
from app.Role.role_model import Role
from app.User.user_repository import (
    read_users,
    read_user,
    create_user,
    delete_user,
    update_user,
    read_users_by_role,
    check_previous_user,
    check_previous_user_edit
)


def read_users_serv(db: Session):
    """Service to get all users."""
    return read_users(db)


def read_user_serv(user_id: int, db: Session):
    """Service to get a user by ID with 404 handling."""
    user = read_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user_serv(user: UserCreate, db: Session):
    """Service to create a new user with full validation."""

    if not user.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")

    if not user.address.strip():
        raise HTTPException(status_code=400, detail="Address is required")

    if not user.username.strip():
        raise HTTPException(status_code=400, detail="Username is required")

    for attr in ["email", "username", "address"]:
        value = getattr(user, attr).strip()
        if check_previous_user(db, attr, value):
            raise HTTPException(
                status_code=400,
                detail=f"{attr.capitalize()} is already registered for another user",
            )

    if not user.role_ids:
        raise HTTPException(
            status_code=400, detail="User must have at least one role assigned"
        )

    roles = db.query(Role).filter(Role.id.in_(user.role_ids)).all()
    if len(roles) != len(set(user.role_ids)):
        raise HTTPException(
            status_code=400, detail="One or more specified roles do not exist"
        )

    user.password = get_password_hash(user.password)

    return create_user(user, roles, db)


def delete_user_serv(user_id: int, db: Session):
    """Service to delete a user by ID with existence check."""
    user = read_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user(user_id, db)


def update_user_serv(user_id: int, user_update: UserCreate, db: Session):
    """Service to update a user by ID."""
    existing_user = read_user_serv(user_id, db)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user_update.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")
    if not user_update.username.strip():
        raise HTTPException(status_code=400, detail="Username is required")
    if not user_update.address.strip():
        raise HTTPException(status_code=400, detail="Address is required")

    for attr in ["email", "username", "address"]:
        value = getattr(user_update, attr).strip()
        if check_previous_user_edit(db, attr, value, exclude_user_id=user_id):
            raise HTTPException(
                status_code=400,
                detail=f"{attr.capitalize()} is already registered for another user",
            )

    if not user_update.role_ids:
        raise HTTPException(status_code=400, detail="User must have at least one role")

    roles = db.query(Role).filter(Role.id.in_(user_update.role_ids)).all()
    if len(roles) != len(set(user_update.role_ids)):
        raise HTTPException(status_code=400, detail="One or more roles do not exist")

    return update_user(user_id, user_update, db)


def read_users_by_role_serv(role_id: int, db: Session):
    """Service to get users by role ID."""
    return read_users_by_role(role_id, db)
