"""Database connection module for FastAPI application."""

from app.db.database import SessionLocal


def get_db():
    """
    Dependency that provides a database session for FastAPI routes.
    Yields:
        Session: A database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
