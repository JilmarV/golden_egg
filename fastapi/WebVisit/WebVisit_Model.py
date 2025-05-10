from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.database import Base

class WebVisit(Base):
    __tablename__ = "web_visit"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
