
from sqlalchemy.orm import Session
from app.repositories.item_repository import create_item, get_item
from app.schemas.item import ItemCreate


def create_new_item(db: Session, item: ItemCreate):
    return create_item(db, item)


def fetch_item(db: Session, item_id: int):
    return get_item(db, item_id)

