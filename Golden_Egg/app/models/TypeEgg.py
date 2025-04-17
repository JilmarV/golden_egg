from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class TypeEgg(Base):
    __tablename__ = "type_egg"

    # Primary Key
    id = Column(BigInteger, primary_key=True)

    name = Column(String)

    # Relación one to many con Egg
    eggs = relationship("Egg", back_populates="type")