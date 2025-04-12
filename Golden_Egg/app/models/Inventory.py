from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(BigInteger, primary_key=True)
    nameProduct = Column(String)
    entryDate = Column(Date)
    expirationDate = Column(Date)
    quantity = Column(BigInteger)

    supplier_id = Column(BigInteger, ForeignKey("supplier.id"))
    #many to one
    supplier = relationship("Supplier", back_populates="inventory")

    egg_id = Column(BigInteger, ForeignKey("egg.id"))
    #one to one
    egg = relationship("Egg", back_populates="inventory")


