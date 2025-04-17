from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.UserRole import UserRole
from app.schemas.UserRole_Schema import UserRoleCreate, UserRoleUpdate

class UserRoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_role(self, user_role_id: int) -> Optional[UserRole]:
        return self.db.query(UserRole).filter(UserRole.id == user_role_id).first()

    def get_user_roles_by_user(self, user_id: int) -> List[UserRole]:
        return self.db.query(UserRole).filter(UserRole.user_id == user_id).all()

    def get_user_roles_by_role(self, role_id: int) -> List[UserRole]:
        return self.db.query(UserRole).filter(UserRole.role_id == role_id).all()

    def create_user_role(self, user_role: UserRoleCreate) -> UserRole:
        db_user_role = UserRole(**user_role.model_dump())
        self.db.add(db_user_role)
        self.db.commit()
        self.db.refresh(db_user_role)
        return db_user_role

    def delete_user_role(self, user_role_id: int) -> bool:
        db_user_role = self.get_user_role(user_role_id)
        if db_user_role:
            self.db.delete(db_user_role)
            self.db.commit()
            return True
        return False