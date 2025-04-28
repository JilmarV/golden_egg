from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True)  # Primary Key
    user_id = Column(Integer, ForeignKey("users.id"))# Foreing Key
    role_id = Column(Integer, ForeignKey("roles.id"))# Foreing Key

    # Many-to-one with User
    user = relationship("User", back_populates="user_role")

    # Many-to-one with Role
    role = relationship("Role", back_populates="user_role")
    