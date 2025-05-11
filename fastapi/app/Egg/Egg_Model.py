from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
from fastapi.app.Supplier.supplier_model import Supplier
from app.OrderEgg.OrderEgg_Model import OrderEgg

class Egg(Base):
    __tablename__ = "egg"

    id = Column(Integer, primary_key=True, index=True)
    nameProduct = Column(String(50), nullable=False)
    avalibleQuantity = Column(Integer, nullable=False)
    entryDate = Column(DateTime, default= datetime.utcnow)
    expirationDate = Column(DateTime, default= datetime.utcnow)
    entryPrice = Column(Float, nullable=False)
    sellPrice = Column(Float, nullable=False)
    color = Column(String(50), nullable=False)
    
    supplier_id = Column(Integer, ForeignKey("supplier.id"))
    supplier = relationship("Supplier", back_populates="eggs")

    order_eggs = relationship("OrderEgg", back_populates="egg")
