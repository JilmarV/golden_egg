from sqlalchemy.orm import Session
from models.TypeEgg import TypeEgg
from schemas.TypeEgg_Schema import TypeEggCreate


def create_TypeEgg(db: Session, typeEgg: TypeEggCreate):
    db_TypeEgg = TypeEgg(**typeEgg.dict())
    db.add(db_TypeEgg)
    db.commit()
    db.refresh(db_TypeEgg)
    return db_TypeEgg

def get_TypeEgg(db: Session, typeEgg_id: int):
    return db.query(TypeEgg).filter(TypeEgg.id == typeEgg_id).first()