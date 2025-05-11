from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from fastapi.app.UserRole.userrole_model import user_role


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)  # Primary Key
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", secondary=user_role, back_populates="roles")