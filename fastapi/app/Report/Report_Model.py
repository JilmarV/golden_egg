from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class Report(Base):
    #Name Of The Table
    __tablename__ = "reports"
    #Unique identifier for the order.
    id = Column(Integer, primary_key=True)
    
    #Type Of Report
    type = Column(String(500))
    
    #Date Of Creation
    dateReport = Column(DateTime, default=datetime.utcnow)
    
    #Content Of The Report
    content = Column(String(50))