from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class Role(Base):
    __tablename__ = "role"

    # Primary Key
    roleId = Column(BigInteger, primary_key=True, index=True)

    roleName = Column(String, nullable=False)

    # One to Many with UserRole
    user_roles = relationship("UserRole", back_populates="role")