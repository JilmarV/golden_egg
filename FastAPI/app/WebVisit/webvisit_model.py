"""SQLAlchemy model for tracking web visits."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base


class WebVisit(Base):
    """Represents a logged visit with IP and timestamp."""

    __tablename__ = "web_visit"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
