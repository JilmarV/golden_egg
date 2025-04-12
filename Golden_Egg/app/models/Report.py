from sqlalchemy import *
from app.db.database import Base

class Report(Base):
    __tablename__ = "report"

    id = Column(BigInteger, primary_key=True, index=True)
    type = Column(String)
    dateReport = Column(Date)
    content = Column(String)
