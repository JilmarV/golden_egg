from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db
from UserRole.UserRole_Repository import *

# Service function to create a new UserRole
def create_user_role_serv(user_id: int, role_id: int, db: Session = Depends(get_db)):
    return create_user_role(user_id, role_id, db)

# Service function to get all UserRoles
def read_user_roles_serv(db: Session = Depends(get_db)):
    return read_user_roles(db)

# Service function to get a specific UserRole by ID
def read_user_role_serv(user_role_id: int, db: Session = Depends(get_db)):
    return read_user_role(user_role_id, db)

# Service function to update a UserRole
def update_user_role_serv(user_role_id: int, user_id: int, role_id: int, db: Session = Depends(get_db)):
    return update_user_role(user_role_id, user_id, role_id, db)

# Service function to delete a UserRole
def delete_user_role_serv(user_role_id: int, db: Session = Depends(get_db)):
    return delete_user_role(user_role_id, db)
