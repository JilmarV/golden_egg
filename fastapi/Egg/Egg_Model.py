from sqlalchemy import Column, Date, Double, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from Supplier.Supplier_Model import Supplier
from Inventory.Inventory_Model import Inventory
from OrderEgg.OrderEgg_Model  import orders_eggs


class Egg(Base):
    __tablename__ = "egg"

    id = Column(Integer, primary_key=True, index=True)
    color = Column(String(50), nullable=False)
    buy_price = Column(Double, nullable=False)
    sale_price = Column(Double, nullable=True)
    expiration_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)

    type_id = Column(Integer, ForeignKey("type_egg.id"), nullable=False)
    type = relationship("TypeEgg", back_populates="eggs")
    
    supplier_id = Column(Integer, ForeignKey("supplier.id"))
    supplier = relationship("Supplier", back_populates="eggs")
    
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    inventory = relationship("Inventory", back_populates="eggs")

    orders = relationship("Order", secondary=orders_eggs, back_populates="eggs")
