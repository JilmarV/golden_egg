from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import HTTPException, Depends
from UserRole_model import *


# Creates a new UserRole in the database
def create_user_role(user_id: int, role_id: int, db: Session):
    db_user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role

# Retrieves all UserRoles from the database
def read_user_roles(db: Session = Depends(get_db)):
    user_roles = db.query(UserRole).all()
    return user_roles

# Retrieves a specific UserRole by its ID
def read_user_role(user_role_id: int, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    if user_role is None:
        raise HTTPException(status_code=404, detail="UserRole not found")
    return user_role

# Updates a UserRole in the database by its ID
def update_user_role(user_role_id: int, user_id: int, role_id: int, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    if user_role is None:
        raise HTTPException(status_code=404, detail="UserRole not found")

    user_role.user_id = user_id
    user_role.role_id = role_id

    db.commit()
    db.refresh(user_role)
    return user_role

# Deletes a UserRole from the database by its ID
def delete_user_role(user_role_id: int, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    if user_role is None:
        raise HTTPException(status_code=404, detail="UserRole not found")
    db.delete(user_role)
    db.commit()
    return {"message": "UserRole deleted successfully"}
