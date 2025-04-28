from sqlalchemy import Column, Integer, String, Date
from db.database import Base

class Report(Base):
    #Name Of The Table
    __tablename__ = "reports"
    #Unique identifier for the order.
    id = Column(Integer, primary_key=True)
    
    #Type Of Report
    type = Column(String)
    
    #Date Of Creation
    dateReport = Column(Date)
    
    #Content Of The Report
    content = Column(String)