"""Repository functions for managing users in the database."""

from app.db.session import get_db
from app.User.user_model import User
from app.Role.role_model import Role
from app.User.user_schema import UserCreate

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException


def create_user(user_data: UserCreate, roles: list[Role], db: Session):
    """Creates a new user and assigns the given roles."""
    db_user = User(
        name=user_data.name,
        phone_number=user_data.phone_number,
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        address=user_data.address,
        enabled=user_data.enabled,
        roles=roles,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_users(db: Session = Depends(get_db)):
    """Retrieves all users from the database."""
    return db.query(User).all()


def read_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific user by its ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    """Updates a user in the database by its ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def check_previous_user(db: Session, field_name: str, value: str):
    """Checks if a user with the given field name and value already exists."""

    return db.query(User).filter(getattr(User, field_name) == value).first()

def check_previous_user_edit(
    db: Session, field_name: str, value: str, exclude_user_id: int = None
):
    """
    Checks if a user with the given field name and value already exists,
    optionally excluding a specific user by ID.
    """
    query = db.query(User).filter(getattr(User, field_name) == value)
    if exclude_user_id is not None:
        query = query.filter(User.id != exclude_user_id)
    return query.first()

def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Deletes a user from the database by its ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


def read_users_by_role(role_id: int, db: Session):
    """Retrieves all users with a specific role."""
    return db.query(User).filter(User.roles.any(Role.id == role_id)).all()


def get_user_by_username(db: Session, username: str) -> User:
    """Retrieve a user by their username."""
    return db.query(User).filter(User.username == username).first()
