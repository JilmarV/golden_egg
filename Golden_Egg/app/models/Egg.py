from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Egg(Base):
    __tablename__ = "egg"

    # Primary Key
    id = Column(BigInteger, primary_key=True, index=True)

    color = Column(String)
    price = Column(Double)

    # Foreign Key to TypeEgg
    type_id = Column(BigInteger, ForeignKey("type_egg.id"))
    # Many to One with TypeEgg
    type = relationship("TypeEgg", back_populates="eggs")

    # One to One with Inventory
    inventory = relationship("Inventory", back_populates="egg", uselist=False)
    # One-to-Many with OrderEggs
    order_eggs = relationship("OrderEggs", back_populates="egg")
