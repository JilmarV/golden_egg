"""SQLAlchemy model for the Pay (payment) table."""

# pylint: disable=too-few-public-methods
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base


class Pay(Base):
    """Represents a payment record."""

    __tablename__ = "payment"

    id = Column(Integer, primary_key=True)  # Unique identifier for the payment
    amount_paid = Column(Float)  # Total amount paid
    payment_method = Column(String(50))  # Payment method
    # Date when the pay was issued.
    issueDate = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"))  # Reference to the user who paid
    user = relationship("User", back_populates="payment")

    bill_id = Column(Integer, ForeignKey("bill.id"))  # Reference to the associated bill
    bill = relationship("Bill", back_populates="payment")
