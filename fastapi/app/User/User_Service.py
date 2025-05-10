from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.User.User_Schema import *
from app.User.User_Repository import *

# Service function to get a list of all users
# It calls the read_users function with the database session
def read_users_serv(db: Session = Depends(get_db)):
    return read_users(db)

# Service function to get a specific user by its ID
# It calls the read_user function with the user ID and database session
def read_user_serv(user_id: int, db: Session = Depends(get_db)):
    return read_user(user_id, db)

# Service function to create a new user
# It calls the create_user function with the user data and the database session
def create_user_serv(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

# Service function to delete a user by its ID
# It calls the delete_user function with the user ID and database session
def delete_user_serv(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)

# Service function to update a user's information by its ID
# It calls the update_user function with the user ID, updated data, and the database session
def update_user_serv(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    return update_user(user_id, user_update, db)
