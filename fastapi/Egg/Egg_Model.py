from sqlalchemy import Column, Date, Double, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.database import Base

#Represents an egg with its attributes.
class Egg(Base):
    __tablename__ = "eggs"

    id = Column(Integer, primary_key=True, index=True)
    
    #Type of egg (e.g., organic, cage-free).
    type_egg = Column(String(50), nullable=False)
    
    #Shell color of the egg.
    color = Column(String(50), nullable=False)
    
    #Expiration date of the egg.
    expirationDate = Column(Date, nullable=False)
    
    #Category or size (e.g., XL, L, M).
    category = Column(String(20), nullable=False)
    
    #Supplier providing the product.
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    supplier = relationship("Supplier", back_populates="eggs")
    
    #Inventory item to which this egg belongs.
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    inventory = relationship("Inventory", back_populates="eggs")