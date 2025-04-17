from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.TypeEgg import TypeEgg
from app.schemas.TypeEgg_Schema import TypeEggCreate, TypeEggUpdate

class TypeEggRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_type_egg(self, type_id: int) -> Optional[TypeEgg]:
        return self.db.query(TypeEgg).filter(TypeEgg.id == type_id).first()

    def get_type_egg_by_name(self, name: str) -> Optional[TypeEgg]:
        return self.db.query(TypeEgg).filter(TypeEgg.name == name).first()

    def get_types_egg(self, skip: int = 0, limit: int = 100) -> List[TypeEgg]:
        return self.db.query(TypeEgg).offset(skip).limit(limit).all()

    def create_type_egg(self, type_egg: TypeEggCreate) -> TypeEgg:
        db_type_egg = TypeEgg(**type_egg.model_dump())
        self.db.add(db_type_egg)
        self.db.commit()
        self.db.refresh(db_type_egg)
        return db_type_egg

    def update_type_egg(self, type_id: int, type_egg: TypeEggUpdate) -> Optional[TypeEgg]:
        db_type_egg = self.get_type_egg(type_id)
        if db_type_egg:
            if type_egg.name is not None:
                db_type_egg.name = type_egg.name
            self.db.commit()
            self.db.refresh(db_type_egg)
        return db_type_egg

    def delete_type_egg(self, type_id: int) -> bool:
        db_type_egg = self.get_type_egg(type_id)
        if db_type_egg:
            self.db.delete(db_type_egg)
            self.db.commit()
            return True
        return False