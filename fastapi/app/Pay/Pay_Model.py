from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.User.User_Model import User
from app.Bill.Bill_Model import Bill

class Pay(Base):
    #Name Of The Table
    __tablename__ = "payment"
    #Unique identifier for the order.
    id = Column(Integer, primary_key=True)
    
    #Total Amount Of The Payment
    amountPaid = Column(Float)
    
    #Payment Method Used By The Client
    paymentMethod = Column(String(50))
    
    #Customer Who Did The Payment
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="payment")
    
    #Bill Associated With The Payment
    bill_id = Column(Integer, ForeignKey("bill.id"))
    bill = relationship("Bill", back_populates="payment")