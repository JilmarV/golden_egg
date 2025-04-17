from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Supplier(Base):
    __tablename__ = "supplier"

    # Primary Key
    id = Column(BigInteger, primary_key=True, index=True)

    name = Column(String)
    address = Column(String)

    #One to Many with Inventory
    inventory_items = relationship("Inventory", back_populates="supplier", cascade="all, delete-orphan")