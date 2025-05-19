"""SQLAlchemy model for the Order table."""

# pylint: disable=too-few-public-methods

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Order(Base):
    """Represents an order record."""

    # Name Of The Table
    __tablename__ = "orders"
    # Unique identifier for the order.
    id = Column(Integer, primary_key=True)

    # Total Price Of The Order
    totalPrice = Column(Float)

    # Date Of Placement Of The Order
    orderDate = Column(DateTime, default=datetime.utcnow)

    # State Of The Order
    state = Column(String(50))

    # many-to-one with User
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")

    bill = relationship("Bill", back_populates="order")

    # one-to.many with Order
    order_eggs = relationship("OrderEgg", back_populates="order")
