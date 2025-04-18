from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class OrderEggs(Base):
    __tablename__ = "order_eggs"

    # Primary Key
    id = Column(BigInteger, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False, default=1)

    # Foreign Key to Order
    order_id = Column(BigInteger, ForeignKey("order.id"))

    # Foreign Key to Egg
    egg_id = Column(BigInteger, ForeignKey("egg.id"))

    # Many to One with Order
    order = relationship("Order", back_populates="order_eggs")

    # Many to One with Egg
    egg = relationship("Egg", back_populates="order_eggs")