from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.Egg import Egg
from app.schemas.Egg_Schema import EggCreate, EggUpdate

class EggRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_egg(self, egg_id: int) -> Optional[Egg]:
        return self.db.query(Egg).filter(Egg.id == egg_id).first()

    def get_eggs_by_type(self, type_id: int) -> List[Egg]:
        return self.db.query(Egg).filter(Egg.type_id == type_id).all()

    def get_eggs(self, skip: int = 0, limit: int = 100) -> List[Egg]:
        return self.db.query(Egg).offset(skip).limit(limit).all()

    def create_egg(self, egg: EggCreate) -> Egg:
        db_egg = Egg(**egg.model_dump())
        self.db.add(db_egg)
        self.db.commit()
        self.db.refresh(db_egg)
        return db_egg

    def update_egg(self, egg_id: int, egg: EggUpdate) -> Optional[Egg]:
        db_egg = self.get_egg(egg_id)
        if db_egg:
            update_data = egg.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_egg, field, value)
            self.db.commit()
            self.db.refresh(db_egg)
        return db_egg

    def delete_egg(self, egg_id: int) -> bool:
        db_egg = self.get_egg(egg_id)
        if db_egg:
            self.db.delete(db_egg)
            self.db.commit()
            return True
        return False