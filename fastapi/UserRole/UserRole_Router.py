from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi.UserRole.UserRole_Service import *

router = APIRouter()

# Endpoint to create a new UserRole
# Accepts user_id and role_id as parameters and returns the created UserRole
@router.post("/user_role/", status_code=201)
def create_user_role_route(user_id: int, role_id: int, db: Session = Depends(get_db)):
    return create_user_role_serv(user_id, role_id, db)

# Endpoint to get a specific UserRole by its ID
# Returns the UserRole matching the provided ID
@router.get("/user_role/{user_role_id}")
def get_user_role_route(user_role_id: int, db: Session = Depends(get_db)):
    return read_user_role_serv(user_role_id, db)

# Endpoint to delete a UserRole by its ID
# Returns a success message once the UserRole is deleted
@router.delete("/user_role/{user_role_id}")
def delete_user_role_route(user_role_id: int, db: Session = Depends(get_db)):
    return delete_user_role_serv(user_role_id, db)

# Endpoint to get a list of all UserRoles
# Returns a list of UserRoles
@router.get("/user_role/")
def read_user_roles_route(db: Session = Depends(get_db)):
    return read_user_roles_serv(db)

# Endpoint to update a UserRole's information by its ID
# Accepts user_id and role_id as parameters to update
@router.put("/user_role/{user_role_id}")
def update_user_role_route(user_role_id: int, user_id: int, role_id: int, db: Session = Depends(get_db)):
    return update_user_role_serv(user_role_id, user_id, role_id, db)
