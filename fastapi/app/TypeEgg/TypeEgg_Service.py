from sqlalchemy.orm import Session
from fastapi import Depends
from app.TypeEgg.TypeEgg_Repository import *
from app.TypeEgg.TypeEgg_Schema import *

# Service function to create a new typeEgg
# Calls the create_typeEgg function from the repository and passes the database session
def create_typeEgg_serv(typeEgg: TypeEggCreate, db: Session = Depends(get_db)):
    return create_typeEgg(typeEgg, db)

# Service function to get a specific typeEgg by its ID
# Calls the read_typeEgg function from the repository and passes the typeEgg ID and database session
def read_typeEgg_serv(typeEgg_id: int, db: Session = Depends(get_db)):
    return read_typeEgg(typeEgg_id, db)

# Service function to get a list of all typeEggs
# Calls the read_typeEggs function from the repository and passes the database session
def read_typeEggs_serv(db: Session = Depends(get_db)):
    return read_typeEggs(db)

# Service function to update a typeEgg by its ID
# Calls the update_typeEgg function from the repository and passes the typeEgg ID, updated data, and database session
def update_typeEgg_serv(typeEgg_id: int, typeEgg_update: TypeEggCreate, db: Session = Depends(get_db)):
    return update_typeEgg(typeEgg_id, typeEgg_update, db)

# Service function to delete a typeEgg by its ID
# Calls the delete_typeEgg function from the repository and passes the typeEgg ID and database session
def delete_typeEgg_serv(typeEgg_id: int, db: Session = Depends(get_db)):
    return delete_typeEgg(typeEgg_id, db)
