from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Pay(Base):
    __tablename__ = "pay"

    # Primary Key
    id = Column(BigInteger, primary_key=True)

    amountPaid = Column(Double)
    paymetMethod = Column(String)

    # Foreign Key a Bill
    bill_id = Column(Integer, ForeignKey("bill.id"))
    # Many-to-One with Bill
    bill = relationship("Bill", back_populates="pay")