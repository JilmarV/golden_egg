from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base
from SupplierTypeEgg.SupplierTypeEgg_Model import Supplier_type

class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    
    eggs = relationship("Egg", back_populates="supplier")
    
    #one-to.many with TypeEgg
    TypeEgg = relationship("TypeEgg", secondary=Supplier_type, back_populates="Supplier")