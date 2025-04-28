from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from Egg.Egg_Schema import *
from Egg.Egg_Model import *

# Create a new egg in the database
def create_egg(egg: EggCreate, db: Session = Depends(get_db)):
    db_egg = Egg(**egg.dict())
    db.add(db_egg)
    db.commit()
    db.refresh(db_egg)
    return db_egg

# Retrieves all eggs from the database
def get_all_eggs(db: Session = Depends(get_db)):
    eggs = db.query(Egg).all()
    return eggs

# Retrieves a specific egg by its ID
def get_egg_by_id(egg_id: int, db: Session = Depends(get_db)):
    egg = db.query(Egg).filter(Egg.id == egg_id).first()
    
    if not egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    return egg

# Updates a specific egg in the database
def update_egg(egg_id: int, egg: EggCreate, db: Session = Depends(get_db)):
    db_egg = db.query(Egg).filter(Egg.id == egg_id).first()
    
    if not db_egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    
    for key, value in egg.dict().items():
        setattr(db_egg, key, value)
    db.commit()
    db.refresh(db_egg)
    return db_egg

# Deletes a specific egg from the database
def delete_egg(egg_id: int, db: Session = Depends(get_db)):
    db_egg = db.query(Egg).filter(Egg.id == egg_id).first()
    
    if not db_egg:
        raise HTTPException(status_code=404, detail="Egg not found")
    
    db.delete(db_egg)
    db.commit()
    return {"message": "Egg deleted successfully"}
