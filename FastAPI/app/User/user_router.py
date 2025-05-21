"""Router for handling user-related API endpoints."""

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
    read_users_by_role_serv,
)

from app.Auth.auth_service import get_current_user, require_admin
from app.User.user_model import User

router = APIRouter()


@router.post("/", status_code=201, response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the database.

    Args:
        user (UserCreate): The user data to create a new user.
        db (Session, optional): The database session dependency.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If the user cannot be created due to validation or database errors.
    """
    return create_user_serv(user, db)


@router.get("/search/me", response_model=UserResponse)
def get_logged_user(current_user: User = Depends(get_current_user)):
    """
    Retrieve the currently authenticated user.

    Args:
        current_user (User): The user object obtained from the authentication dependency.

    Returns:
        User: The currently authenticated user.
    """
    return current_user


@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_admin)])
def get_user_route(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a user by their user ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session, optional): SQLAlchemy database session dependency.

    Returns:
        User: The user object corresponding to the provided user_id.

    Raises:
        HTTPException: If the user does not exist or the current user lacks admin privileges.
    """
    return read_user_serv(user_id, db)


@router.delete("/{user_id}", response_model=dict, dependencies=[Depends(require_admin)])
def delete_user_route(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Deletes a user from the database based on the provided user ID.

    Args:
        user_id (int): The unique identifier of the user to be deleted.
        db (Session, optional): SQLAlchemy database session dependency.

    Returns:
        Any: The result of the delete operation, as returned by the delete_user_serv function.
    """
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
    """
    Update an existing user's information.

    Args:
        user_id (int): The ID of the user to update.
        user_update (UserCreate): The new data for the user.
        db (Session, optional): Database session dependency.

    Returns:
        The updated user object or the result of the update operation.
    """
    return update_user_serv(user_id, user_update, db)


@router.get("/byrole/{role_id}", response_model=List[UserResponse], dependencies=[Depends(require_admin)])
def get_users_by_role(
    role_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a list of users filtered by their role ID.

    Args:
        role_id (int): The ID of the role to filter users by.
        db (Session, optional): SQLAlchemy database session dependency. Defaults to Depends(get_db).

    Returns:
        List[User]: A list of user objects associated with the specified role.
    """
    return read_users_by_role_serv(role_id, db)
