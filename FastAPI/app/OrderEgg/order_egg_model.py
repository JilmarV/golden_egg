"""SQLAlchemy model for the Order_Egg table."""

# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base


class OrderEgg(Base):
    """Represents an order-egg relationship in the database."""

    __tablename__ = "order_egg"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    sub_total = Column(Float, nullable=False)

    egg_id = Column(Integer, ForeignKey("egg.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    egg = relationship("Egg", back_populates="order_eggs")
    order = relationship("Order", back_populates="order_eggs")
