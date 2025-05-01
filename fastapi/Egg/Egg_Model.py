from sqlalchemy import Column, Date, Double, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from Supplier.Supplier_Model import Supplier
from Inventory.Inventory_Model import Inventory
from OrderEgg.OrderEgg_Model  import orders_eggs


class Egg(Base):
    __tablename__ = "egg"

    id = Column(Integer, primary_key=True, index=True)
    type_egg = Column(String(50), nullable=False)
    color = Column(String(50), nullable=False)
    expirationDate = Column(Date, nullable=False)
    category = Column(String(20), nullable=False)
    
    supplier_id = Column(Integer, ForeignKey("supplier.id"))
    supplier = relationship("Supplier", back_populates="eggs")
    
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    inventory = relationship("Inventory", back_populates="eggs")

    orders = relationship("Order", secondary=orders_eggs, back_populates="eggs")
