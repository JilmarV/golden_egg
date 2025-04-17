from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.User import User
from app.schemas.User_Schema import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> Optional[User]:
        #Obtiene un usuario por su id
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        #Obtiene un usuario por su email
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        #Obtiene un usuario por su nombre de usuario
        return self.db.query(User).filter(User.userName == username).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        #Obtiene una lista de usuarios con paginación
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate) -> User:
        #Crea un nuevo usuario (sin hashing de contraseña)
        db_user = User(
            email=user.email,
            userName=user.userName,
            name=user.name,
            phoneNumber=user.phoneNumber,
            hashed_password=user.password,
            address=user.address,
            enabled=user.enabled
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        #Actualiza un usuario existente
        db_user = self.get_user(user_id)
        if db_user:
            update_data = user_update.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(db_user, field, value)

            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        #Elimina un usuario
        db_user = self.get_user(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
