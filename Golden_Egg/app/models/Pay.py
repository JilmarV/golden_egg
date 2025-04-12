from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Pay(Base):
    __tablename__ = "pay"

    id = Column(BigInteger, primary_key=True)

    amountPaid = Column(Double)
    paymetMethod = Column(String)

    client_id = Column(Integer, ForeignKey("client.id"))
    #one to one
    client = relationship("Client", back_populates="pay")

    bill_id = Column(Integer, ForeignKey("bill.id"))
    #many to one
    bill = relationship("Bill", back_populates="pay")

