from sqlalchemy import Column, Date, Double, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.database import Base

# Represents a bill issued for an order.

class Bill(Base):
    __tablename__ = "bills"

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
