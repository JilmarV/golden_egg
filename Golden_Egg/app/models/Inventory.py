from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    # Primary Key
    id = Column(BigInteger, primary_key=True)

    nameProduct = Column(String)
    entryDate = Column(Date)
    expirationDate = Column(Date)
    quantity = Column(BigInteger)

    # Foreign Key to Supplier
    supplier_id = Column(BigInteger, ForeignKey("supplier.id"))
    # Many to One with Supplier
    supplier = relationship("Supplier", back_populates="inventory_items")

    # Foreign Key to Egg
    egg_id = Column(BigInteger, ForeignKey("egg.id"))
    # One to One with Egg
    egg = relationship("Egg", back_populates="inventory")