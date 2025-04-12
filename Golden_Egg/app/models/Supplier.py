from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)

    #one to many
    inventory_items = relationship("Inventory", back_populates="supplier", cascade="all, delete-orphan")

