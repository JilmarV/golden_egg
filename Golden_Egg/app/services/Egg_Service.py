from sqlalchemy.orm import Session
from repositories.Egg_Repository import create_Egg, get_Egg
from schemas.Egg_Schema import EggCreate


def create_new_egg(db: Session, egg: EggCreate):
    return create_Egg(db, egg)


def fetch_egg(db: Session, egg_id: int):
    return get_Egg(db, egg_id)