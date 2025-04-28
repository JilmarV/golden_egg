from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # Primary Key
    name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    address = Column(String)
    enabled = Column(Boolean)

    # One-to-many with UserRole
    user_role = relationship("UserRole", back_populates="user", cascade="all, delete")