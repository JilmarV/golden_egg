from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class UserRole(Base):
    __tablename__ = "user_role"

    # Primary Key
    id = Column(BigInteger, primary_key=True, index=True)

    # Foreign Key to Role
    role_id = Column(BigInteger, ForeignKey("role.roleId"))

    # Foreign Key to User
    user_id = Column(BigInteger, ForeignKey("user.id"))

    # Many to One with Role
    role = relationship("Role", back_populates="user_roles")

    # Many to One with User
    user = relationship("User", back_populates="roles")