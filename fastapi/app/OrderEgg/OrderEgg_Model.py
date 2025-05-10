from sqlalchemy import Table, Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class OrderEgg(Base):
    __tablename__ = "order_egg"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    sub_total = Column(Float, nullable=False)
    
    egg_id = Column(Integer, ForeignKey("egg.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    
    egg = relationship("Egg", back_populates="order_eggs")
    order = relationship("Order", back_populates="order_eggs")