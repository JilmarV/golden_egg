from sqlalchemy import Column, Date, Double, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.database import Base

#Represents an inventory item in the system.
class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    
    #Name of the inventory item.
    nameProduct = Column(String(50), nullable=False)
    
    #Quantity currently available in stock.
    availableQuantity = Column(String, nullable=False)
    
    #Unit price of the product.
    price = Column(Double, nullable=False)
    
    #Date the product was added to inventory.
    entryDate = Column(Date, nullable=False)
    
    #List of eggs associated with this inventory item.
    eggs = relationship("Egg", back_populates="inventory")