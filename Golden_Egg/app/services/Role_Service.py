from sqlalchemy.orm import Session
from repositories.Role_Repository import create_Role, get_Role
from schemas.Role_Schema import RoleCreate


def create_new_role(db: Session, role: RoleCreate):
    return create_Role(db, role)


def fetch_role(db: Session, role_id: int):
    return get_Role(db, role_id)