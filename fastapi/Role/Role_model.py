from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)  # Primary Key
    name = Column(String, unique=True, nullable=False)

    # One-to-many with UserRole
    user_role = relationship("UserRole", back_populates="role", cascade="all, delete")