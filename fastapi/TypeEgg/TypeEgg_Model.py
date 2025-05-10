from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base
from SupplierTypeEgg.SupplierTypeEgg_Model import Supplier_type

class TypeEgg(Base):
    __tablename__ = "type_egg"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    
    #one-to.many with TypeEgg
    Supplier = relationship("Supplier", secondary=Supplier_type, back_populates="TypeEgg")