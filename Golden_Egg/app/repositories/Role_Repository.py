from sqlalchemy.orm import Session
from models.Role import Role
from schemas.Role_Schema import RoleCreate


def create_Role(db: Session, role: RoleCreate):
    db_Role = Role(**role.dict())
    db.add(db_Role)
    db.commit()
    db.refresh(db_Role)
    return db_Role

def get_Role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()