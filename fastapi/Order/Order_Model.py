from sqlalchemy import Column, Integer, ForeignKey, String, Date, Float
from sqlalchemy.orm import relationship
from db.database import Base
from User.User_Model import User
from OrderEgg.OrderEgg_Model import orders_eggs

class Order(Base):
    #Name Of The Table
    __tablename__ = "orders"
    #Unique identifier for the order.
    id = Column(Integer, primary_key=True)
    
    #Total Price Of The Order
    totalPrice = Column(Float)
    
    #Date Of Placement Of The Order
    orderDate = Column(Date)
    
    #State Of The Order
    state = Column(String)
    
    #many-to-one with User
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")
    
    bill = relationship("Bill", back_populates="order", uselist=False)

    #one-to.many with Order
    eggs = relationship("Egg", secondary=orders_eggs, back_populates="orders")