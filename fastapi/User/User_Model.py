from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from UserRole.UserRole_Model import user_role


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)  # Primary Key
    name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    address = Column(String)
    enabled = Column(Boolean)

    orders = relationship("Order", back_populates="user")
    
    roles = relationship("Role", secondary=user_role, back_populates="users")
    
    payment = relationship("Pay", back_populates="user", uselist=False)
