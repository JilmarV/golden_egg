from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Bill(Base):
    __tablename__ = "bill"

    # Primary Key
    id = Column(BigInteger, primary_key=True)

    issueDate = Column(Date)
    totalPrice = Column(Double)
    paid = Column(Boolean)

    # Foreign Key to Order
    order_id = Column(BigInteger, ForeignKey("order.id"))
    # One to One with Order
    order = relationship("Order", back_populates="bill")

    # One to Many relationship with Pay
    pays = relationship("Pay", back_populates="bill", cascade="all, delete-orphan")