from sqlalchemy.orm import Session
from models.User import User
from schemas.User_Schema import UserCreate


def create_User(db: Session, user: UserCreate):
    db_User = User(**user.dict())
    db.add(db_User)
    db.commit()
    db.refresh(db_User)
    return db_User

def get_User(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()