from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class TypeEgg(Base):
    __tablename__ = "type_egg"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)

    egg_id = Column(BigInteger, ForeignKey("egg.id"))
    #one to one
    egg = relationship("Egg", back_populates="type_egg")

