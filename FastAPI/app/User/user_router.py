"""Router for handling user-related API endpoints."""

# pylint: disable=import-error, no-name-in-module

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.User.user_schema import UserCreate, UserResponse
from app.User.user_service import (
    create_user_serv,
    read_user_serv,
    delete_user_serv,
    read_users_serv,
    update_user_serv,
    read_users_by_role_serv
)

from app.Auth.auth_service import get_current_user, require_admin
from app.User.user_model import User

router = APIRouter()


@router.post("/", status_code=201, response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """Creates a new user."""
    return create_user_serv(user, db)


@router.get("/search/me", response_model=UserResponse)
def get_logged_user(current_user: User = Depends(get_current_user)):
    """Returns the currently authenticated user."""
    return current_user


@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_admin)])
def get_user_route(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Retrieves a user by ID."""
    return read_user_serv(user_id, db)


@router.delete("/{user_id}", response_model=dict, dependencies=[Depends(require_admin)])
def delete_user_route(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Deletes a user by ID."""
    return delete_user_serv(user_id, db)


@router.get("/", response_model=List[UserResponse], dependencies=[Depends(require_admin)])
def read_users_route(
    db: Session = Depends(get_db),
):
    """Retrieves all users."""
    return read_users_serv(db)


@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_admin)])
def update_user_route(
    user_id: int,
    user_update: UserCreate,
    db: Session = Depends(get_db),
):
    """Updates a user by ID."""
    return update_user_serv(user_id, user_update, db)


@router.get("/byrole/{role_id}", response_model=List[UserResponse], dependencies=[Depends(require_admin)])
def get_users_by_role(
    role_id: int,
    db: Session = Depends(get_db),
):
    """Selects users by Role."""
    return read_users_by_role_serv(role_id, db)
