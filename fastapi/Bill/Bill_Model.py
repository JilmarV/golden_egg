from sqlalchemy import Column, Date, Double, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from Order.Order_Model import Order

class Bill(Base):
    __tablename__ = "bill"

    id = Column(Integer, primary_key=True, index=True)
    
    # Date when the bill was issued.
    issueDate = Column(Date, nullable=False)
    
    # Total price to be paid.
    totalprice = Column(Double, nullable=False)
    
    # Whether the bill has been paid.
    paid = Column(Boolean, nullable=False)
    
    # Associated order for this bill.
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="bill")

    payment = relationship("Pay", back_populates="bill", uselist=False)


