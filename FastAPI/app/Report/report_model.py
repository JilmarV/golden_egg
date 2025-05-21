"""SQLAlchemy model for the Report entity."""

# pylint: disable=too-few-public-methods
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base


class Report(Base):
    """Represents a report stored in the system."""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)  # Unique identifier for the report
    type = Column(String(500))  # Type of the report
    dateReport = Column(DateTime, default=datetime.utcnow)  # Report creation date
    content = Column(String(50))  # Content or description of the report
