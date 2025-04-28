from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from db.database import Base

class Pay(Base):
    #Name Of The Table
    __tablename__ = "payments"
    #Unique identifier for the order.
    id = Column(Integer, primary_key=True)
    
    #Total Amount Of The Payment
    amountPaid = Column(Float)
    
    #Payment Method Used By The Client
    paymentMethod = Column(String)
    
    #Customer Who Did The Payment
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="payments")
    
    #Bill Associated With The Payment
    bill_id = Column(Integer, ForeignKey("bill.id"))
    bill = relationship("Bill", back_populates="payments")