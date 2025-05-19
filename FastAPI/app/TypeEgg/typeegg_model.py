"""SQLAlchemy model for the egg type (TypeEgg)."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class TypeEgg(Base):
    """Represents an egg type in the system."""

    __tablename__ = "typeEgg"

    id = Column(Integer, primary_key=True)  # Primary key
    name = Column(String(50), unique=True, nullable=False)

    eggs = relationship("Egg", back_populates="type_egg")
