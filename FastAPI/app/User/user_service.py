"""Service layer for user-related operations."""

# pylint: disable=no-name-in-module

from sqlalchemy.orm import Session
from app.User.user_schema import UserCreate
from app.User.user_repository import (
    read_users,
    read_user,
    create_user,
    delete_user,
    update_user,
    read_users_by_role,
)


def read_users_serv(db: Session):
    """Service to get all users."""
    return read_users(db)


def read_user_serv(user_id: int, db: Session):
    """Service to get a user by ID."""
    return read_user(user_id, db)


def create_user_serv(user: UserCreate, db: Session):
    """Service to create a new user."""
    return create_user(user, db)


def delete_user_serv(user_id: int, db: Session):
    """Service to delete a user by ID."""
    return delete_user(user_id, db)


def update_user_serv(user_id: int, user_update: UserCreate, db: Session):
    """Service to update a user by ID."""
    return update_user(user_id, user_update, db)


def read_users_by_role_serv(role_id: int, db: Session):
    """Service to get users by role ID."""
    return read_users_by_role(role_id, db)
