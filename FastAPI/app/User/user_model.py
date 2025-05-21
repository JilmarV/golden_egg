"""SQLAlchemy model for the User entity in the system."""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.UserRole.userrole_model import user_role


class User(Base):
    """Represents a user of the system."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)  # Primary Key
    name = Column(String(50))
    phone_number = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    address = Column(String(50), unique=True)
    enabled = Column(Boolean)

    orders = relationship("Order", back_populates="user")
    roles = relationship("Role", secondary=user_role, back_populates="users")
    payment = relationship("Pay", back_populates="user", uselist=False)
