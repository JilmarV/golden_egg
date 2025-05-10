from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import Depends, HTTPException
from app.TypeEgg.TypeEgg_Model import *
from app.TypeEgg.TypeEgg_Schema import *

# Creates a new typeEgg in the database
def create_typeEgg(typeEgg: TypeEggCreate, db: Session):
    db_typeEgg = TypeEgg(**typeEgg.dict())
    db.add(db_typeEgg)
    db.commit()
    db.refresh(db_typeEgg)
    return db_typeEgg

# Retrieves all typeEggs from the database
def read_typeEggs(db: Session = Depends(get_db)):
    typeEggs = db.query(TypeEgg).all()
    return typeEggs

# Retrieves a specific typeEgg by its ID
def read_typeEgg(typeEgg_id: int, db: Session = Depends(get_db)):
    typeEgg = db.query(TypeEgg).filter(TypeEgg.id == typeEgg_id).first()
    if typeEgg is None:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    return typeEgg

# Updates a typeEgg in the database by its ID
def update_typeEgg(typeEgg_id: int, typeEgg_update: TypeEggCreate, db: Session = Depends(get_db)):
    typeEgg = db.query(TypeEgg).filter(TypeEgg.id == typeEgg_id).first()
    if typeEgg is None:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    
    for key, value in typeEgg_update.dict(exclude_unset=True).items():
        setattr(typeEgg, key, value)
    
    db.commit()
    db.refresh(typeEgg)
    return typeEgg

# Deletes a typeEgg from the database by its ID
def delete_typeEgg(typeEgg_id: int, db: Session = Depends(get_db)):
    typeEgg = db.query(TypeEgg).filter(TypeEgg.id == typeEgg_id).first()
    if typeEgg is None:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    db.delete(typeEgg)
    db.commit()
    return {"message": "TypeEgg deleted successfully"}