from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from User.User_Model import *
from User.User_Schema import *
from User.User_Service import *

router = APIRouter()

# Endpoint to create a new user
# Accepts a UserCreate object and returns a UserResponse with the created user
@router.post("/user/", status_code=201, response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_serv(user, db)

# Endpoint to get a specific user by its ID
# Returns the user matching the provided ID
@router.get("/user/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    return read_user_serv(user_id, db)

# Endpoint to delete a user by its ID
# Returns a success message once the user is deleted
@router.delete("/user/{user_id}", response_model=dict)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    return delete_user_serv(user_id, db)

# Endpoint to get a list of all users
# Returns a list of users
@router.get("/user/", response_model=list[UserResponse])
def read_users_route(db: Session = Depends(get_db)):
    return read_users_serv(db)

# Endpoint to update a user's information by its ID
# Accepts a UserCreate object with the updated data
@router.put("/user/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    return update_user_serv(user_id, user_update, db)