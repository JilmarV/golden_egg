from sqlalchemy.orm import Session
from fastapi import Depends
from Role.Role_Repository import *
from Role.Role_Schema import *

# Service function to create a new role
# Calls the create_role function from the repository and passes the database session
def create_role_serv(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(role, db)

# Service function to get a specific role by its ID
# Calls the read_role function from the repository and passes the role ID and database session
def read_role_serv(role_id: int, db: Session = Depends(get_db)):
    return read_role(role_id, db)

# Service function to get a list of all roles
# Calls the read_roles function from the repository and passes the database session
def read_roles_serv(db: Session = Depends(get_db)):
    return read_roles(db)

# Service function to update a role by its ID
# Calls the update_role function from the repository and passes the role ID, updated data, and database session
def update_role_serv(role_id: int, role_update: RoleCreate, db: Session = Depends(get_db)):
    return update_role(role_id, role_update, db)

# Service function to delete a role by its ID
# Calls the delete_role function from the repository and passes the role ID and database session
def delete_role_serv(role_id: int, db: Session = Depends(get_db)):
    return delete_role(role_id, db)
