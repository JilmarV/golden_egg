from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Egg(Base):
    __tablename__ = "egg"

    id = Column(BigInteger, primary_key=True, index=True)
    color = Column(String)
    price = Column(Double)

    type_id = Column(BigInteger, ForeignKey("type_egg.id"))
    # one to one
    type = relationship("TypeEgg", back_populates="egg")

