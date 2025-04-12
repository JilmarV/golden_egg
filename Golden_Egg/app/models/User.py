from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    userName = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String)
    enabled = Column(Boolean, default=True)

    # one to many
    roles = relationship("UserRole", back_populates="user")
