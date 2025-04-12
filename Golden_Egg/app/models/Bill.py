from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Bill(Base):
    __tablename__ = "bill"

    id = Column(BigInteger, primary_key=True)
    issueDate = Column(Date)
    totalPrice = Column(Double)
    paid = Column(Boolean)

    #one to one
    order_id = Column(BigInteger, ForeignKey("order.id"))
    order = relationship("Order", back_populates="bill")

    #one to many
    pays = relationship("Pay", back_populates="bill", cascade="all, delete-orphan")