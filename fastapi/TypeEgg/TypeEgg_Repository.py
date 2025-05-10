from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from db.session import get_db
from TypeEgg.TypeEgg_Model import TypeEgg
from TypeEgg.TypeEgg_Schema import TypeEggCreate

# Create a new TypeEgg
def create_type_egg(type_egg: TypeEggCreate, db: Session):
    db_type_egg = TypeEgg(**type_egg.dict())
    db.add(db_type_egg)
    db.commit()
    db.refresh(db_type_egg)
    return db_type_egg

# Retrieve all TypeEgg records
def read_type_eggs(db: Session = Depends(get_db)):
    return db.query(TypeEgg).all()

# Retrieve a specific TypeEgg by ID
def read_type_egg(type_egg_id: int, db: Session = Depends(get_db)):
    type_egg = db.query(TypeEgg).filter(TypeEgg.id == type_egg_id).first()
    if type_egg is None:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    return type_egg

# Update an existing TypeEgg by ID
def update_type_egg(type_egg_id: int, type_egg_update: TypeEggCreate, db: Session = Depends(get_db)):
    type_egg = db.query(TypeEgg).filter(TypeEgg.id == type_egg_id).first()
    if type_egg is None:
        raise HTTPException(status_code=404, detail="TypeEgg not found")

    for key, value in type_egg_update.dict(exclude_unset=True).items():
        setattr(type_egg, key, value)

    db.commit()
    db.refresh(type_egg)
    return type_egg

# Delete a TypeEgg by ID
def delete_type_egg(type_egg_id: int, db: Session = Depends(get_db)):
    type_egg = db.query(TypeEgg).filter(TypeEgg.id == type_egg_id).first()
    if type_egg is None:
        raise HTTPException(status_code=404, detail="TypeEgg not found")
    db.delete(type_egg)
    db.commit()
    return {"message": "TypeEgg deleted successfully"}
