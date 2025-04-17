from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Order(Base):
    __tablename__ = "order"

    # Primary Key
    id = Column(BigInteger, primary_key=True, index=True)
    totalPrice = Column(Float)
    orderDate = Column(Date)
    state = Column(String)

    # Many to Many with order_eggs
    eggs = relationship("Egg", secondary="order_eggs", back_populates="orders")

    # One to One with Bill
    bill = relationship("Bill", back_populates="order", uselist=False)