"""SQLAlchemy model for the User entity in the system."""

# pylint: disable=import-error, too-few-public-methods

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
from fastapi.app.UserRole.userrole_model import user_role


class User(Base):
    """Represents a user of the system."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)  # Primary Key
    name = Column(String(50))
    phone_number = Column(String(50))
    email = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))
    address = Column(String(50))
    enabled = Column(Boolean)

    orders = relationship("Order", back_populates="user")
    roles = relationship("Role", secondary=user_role, back_populates="users")
    payment = relationship("Pay", back_populates="user", uselist=False)
