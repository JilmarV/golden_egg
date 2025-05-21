"""Repository functions for managing roles in the database."""

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.Role.role_model import Role
from app.Role.role_schema import RoleCreate
from fastapi import Depends, HTTPException


def create_role(role: RoleCreate, db: Session):
    """Creates a new role in the database."""
    db_role = Role(**role.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def read_roles(db: Session = Depends(get_db)):
    """Retrieves all roles from the database."""
    return db.query(Role).all()


def read_role(role_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific role by its ID."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


def update_role(role_id: int, role_update: RoleCreate, db: Session = Depends(get_db)):
    """Updates a role by its ID."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    for key, value in role_update.model_dump(exclude_unset=True).items():
        setattr(role, key, value)

    db.commit()
    db.refresh(role)
    return role


def delete_role(role_id: int, db: Session = Depends(get_db)):
    """Deletes a role by its ID."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}


def check_previous_role(db: Session, field_name: str, value: str):
    """Checks if a role with the given field name and value exists in the database."""
    return db.query(Role).filter(getattr(Role, field_name) == value).first()
