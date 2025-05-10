from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import Depends, HTTPException
from app.Role.Role_Model import *
from app.Role.Role_Schema import *

# Creates a new role in the database
def create_role(role: RoleCreate, db: Session):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# Retrieves all roles from the database
def read_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles

# Retrieves a specific role by its ID
def read_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Updates a role in the database by its ID
def update_role(role_id: int, role_update: RoleCreate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    
    for key, value in role_update.dict(exclude_unset=True).items():
        setattr(role, key, value)
    
    db.commit()
    db.refresh(role)
    return role

# Deletes a role from the database by its ID
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}