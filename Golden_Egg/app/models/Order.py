from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Order(Base):
    __tablename__ = "order"

    # Primary Key
    id = Column(BigInteger, primary_key=True, index=True)
    totalPrice = Column(Double)
    orderDate = Column(Date)
    state = Column(String)
    #Foreign Key to User
    user_id = Column(BigInteger, ForeignKey("user.id"))

    # One to One with Bill
    bill = relationship("Bill", back_populates="order", uselist=False)
    # One to Many with OrderEggs
    order_eggs = relationship("OrderEggs", back_populates="order")
    #One to Many with User
    user = relationship("User", back_populates="orders")
