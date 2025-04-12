from sqlalchemy.orm import Session
from repositories.User_Repository import create_User, get_User
from schemas.User_Schema import UserCreate


def create_new_user(db: Session, user: UserCreate):
    return create_User(db, user)


def fetch_user(db: Session, user_id: int):
    return get_User(db, user_id)