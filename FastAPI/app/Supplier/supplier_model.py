"""SQLAlchemy model for egg suppliers."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Supplier(Base):
    """Represents a supplier who provides eggs."""

    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)

    eggs = relationship("Egg", back_populates="supplier")
