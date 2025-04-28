from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

#Class To Map The Many To Many Relationship
class Order_Egg(Base):
    #Name Of The Table
    __tablename__ = "orders_eggs"
    
    #Unique Identifier For The Table.
    id = Column(Integer, primary_key=True)
    
    #Relation Many To Many Between Eggs And Orders
    order_id = Column("order_id", Integer, ForeignKey("order.id"), primary_key=True)
    order = relationship("Order", back_populates="order_eggs")
    egg_id = Column("egg_id", Integer, ForeignKey("egg.id"), primary_key=True)
    egg = relationship("Egg", back_populates="order_eggs")