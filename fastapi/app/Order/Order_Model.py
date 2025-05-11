from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
from app.User.User_Model import User
from app.OrderEgg.OrderEgg_Model import OrderEgg

class Order(Base):
    #Name Of The Table
    __tablename__ = "orders"
    #Unique identifier for the order.
    id = Column(Integer, primary_key=True)
    
    #Total Price Of The Order
    totalPrice = Column(Float)
    
    #Date Of Placement Of The Order
    orderDate = Column(DateTime, default=datetime.utcnow)

    #State Of The Order
    state = Column(String(50))
    
    #many-to-one with User
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")
    
    bill = relationship("Bill", back_populates="order", uselist=False)

    #one-to.many with Order
    order_eggs = relationship("OrderEgg", back_populates="order")
    