from sqlalchemy import Column, Integer, String, Date, Double
from sqlalchemy.orm import relationship
from db.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    nameProduct = Column(String(50), nullable=False)
    entryDate = Column(Date, nullable=False)
    
    eggs = relationship("Egg", back_populates="inventory")