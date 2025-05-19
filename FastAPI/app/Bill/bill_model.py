"""SQLAlchemy model for the Bill table."""

# pylint: disable=too-few-public-methods

from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base


class Bill(Base):
    """Model representing a bill in the database."""

    __tablename__ = "bill"

    id = Column(Integer, primary_key=True, index=True)

    # Date when the bill was issued.
    issueDate = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Total price to be paid.
    totalprice = Column(Float, nullable=False)

    # Whether the bill has been paid.
    paid = Column(Boolean, nullable=False)

    # Associated order for this bill.
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="bill")

    payment = relationship("Pay", back_populates="bill")
