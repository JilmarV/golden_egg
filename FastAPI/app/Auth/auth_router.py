"""This module defines the authentication routes for the FastAPI application."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.Auth.auth_service import create_access_token, verify_password
from app.User.user_repository import get_user_by_username

router = APIRouter()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Authenticate a user and generate a JWT access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        dict: A dictionary containing the access token and its type.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
    """
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": user.username}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}
