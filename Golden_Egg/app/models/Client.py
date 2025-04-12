from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Client(Base):
    __tablename__ = "client"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(String)
    enabled = Column(Boolean, default=True)

    #One to many
    order = relationship("Order", back_populates="client", cascade="all, delete-orphan")
    # One to many
    pay = relationship("Pay", back_populates="client", cascade="all, delete-orphan")

