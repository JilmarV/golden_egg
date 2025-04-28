from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from Role.Role_Schema import *
from Role.Role_Service import *

router = APIRouter()

# Endpoint to create a new role
# Accepts a RoleCreate object and returns a RoleResponse with the created role
@router.post("/role/", status_code=201, response_model=RoleResponse)
def create_role_route(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role_serv(role, db)

# Endpoint to get a specific role by its ID
# Returns the role matching the provided ID
@router.get("/role/{role_id}", response_model=RoleResponse)
def get_role_route(role_id: int, db: Session = Depends(get_db)):
    return read_role_serv(role_id, db)

# Endpoint to get a list of all roles
# Returns a list of roles
@router.get("/roles/", response_model=list[RoleResponse])
def get_roles_route(db: Session = Depends(get_db)):
    return read_roles_serv(db)

# Endpoint to update a role's information by its ID
# Accepts a RoleCreate object with the updated data
@router.put("/role/{role_id}", response_model=RoleResponse)
def update_role_route(role_id: int, role_update: RoleCreate, db: Session = Depends(get_db)):
    return update_role_serv(role_id, role_update, db)

# Endpoint to delete a role by its ID
# Returns a success message once the role is deleted
@router.delete("/role/{role_id}")
def delete_role_route(role_id: int, db: Session = Depends(get_db)):
    return delete_role_serv(role_id, db)
