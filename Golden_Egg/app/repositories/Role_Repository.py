from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.Role import Role
from app.schemas.Role_Schema import RoleCreate, RoleUpdate

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_role(self, role_id: int) -> Optional[Role]:
        return self.db.query(Role).filter(Role.roleId == role_id).first()

    def get_role_by_name(self, role_name: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.roleName == role_name).first()

    def get_roles(self, skip: int = 0, limit: int = 100) -> List[Role]:
        return self.db.query(Role).offset(skip).limit(limit).all()

    def create_role(self, role: RoleCreate) -> Role:
        db_role = Role(roleName=role.roleName)
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def update_role(self, role_id: int, role: RoleUpdate) -> Optional[Role]:
        db_role = self.get_role(role_id)
        if db_role:
            if role.roleName is not None:
                db_role.roleName = role.roleName
            self.db.commit()
            self.db.refresh(db_role)
        return db_role

    def delete_role(self, role_id: int) -> bool:
        db_role = self.get_role(role_id)
        if db_role:
            self.db.delete(db_role)
            self.db.commit()
            return True
        return False