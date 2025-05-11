"""Repository functions for managing users in the database."""

# pylint: disable=import-error, no-name-in-module

from app.db.session import get_db
from app.User.user_model import User
from app.User.user_schema import UserCreate

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException


def create_user(user: UserCreate, db: Session):
    """Creates a new user in the database."""
    db_user = User(**user.dict())
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


def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Deletes a user from the database by its ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
