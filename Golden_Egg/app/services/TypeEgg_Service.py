from sqlalchemy.orm import Session
from repositories.TypeEgg_Repository import create_TypeEgg, get_TypeEgg
from schemas.TypeEgg_Schema import TypeEggCreate


def create_new_typeEgg(db: Session, typeEgg: TypeEggCreate):
    return create_TypeEgg(db, typeEgg)


def fetch_typeEgg(db: Session, typeEgg_id: int):
    return get_TypeEgg(db, typeEgg_id)