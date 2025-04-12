from sqlalchemy.orm import Session
from models.Egg import Egg
from schemas.Egg_Schema import EggCreate

def create_Egg(db: Session, egg: EggCreate):
    db_Egg = Egg(**egg.dict())
    db.add(db_Egg)
    db.commit()
    db.refresh(db_Egg)
    return db_Egg

def get_Egg(db: Session, egg_id: int):
    return db.query(Egg).filter(Egg.id == egg_id).first()