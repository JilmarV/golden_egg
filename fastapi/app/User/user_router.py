"""Router for handling user-related API endpoints."""

# pylint: disable=import-error, no-name-in-module

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.User.user_schema import UserCreate, UserResponse
from app.User.user_service import (
    create_user_serv,
    read_user_serv,
    delete_user_serv,
    read_users_serv,
    update_user_serv,
    read_users_by_role
)

from fastapi import APIRouter, Depends


router = APIRouter()


@router.post("/user/", status_code=201, response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """Creates a new user."""
    return create_user_serv(user, db)


@router.get("/user/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    """Retrieves a user by ID."""
    return read_user_serv(user_id, db)


@router.delete("/user/{user_id}", response_model=dict)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    """Deletes a user by ID."""
    return delete_user_serv(user_id, db)


@router.get("/user/", response_model=list[UserResponse])
def read_users_route(db: Session = Depends(get_db)):
    """Retrieves all users."""
    return read_users_serv(db)


@router.put("/user/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    """Updates a user by ID."""
    return update_user_serv(user_id, user_update, db)

@router.get("/user/byrole/{role_id}", response_model = UserResponse)
def get_users_by_role(role_id: id, db: Session = Depends(get_db)):
    return read_users_by_role(role_id, db)
