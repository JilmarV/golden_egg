from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Order(Base):
    __tablename__ = "order"

    id = Column(BigInteger, primary_key=True, index=True)
    totalPrice = Column(Float)
    orderDate = Column(Date)
    state = Column(String)

    client_id = Column(BigInteger, ForeignKey("client.id"))

    #many to many
    eggs = relationship("Egg", secondary="order_egg", back_populates="order ")

    #one to many
    bill = relationship("Bill", back_populates="order", uselist=False)
