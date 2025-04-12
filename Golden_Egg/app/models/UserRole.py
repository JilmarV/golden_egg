from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(BigInteger, primary_key=True, index=True)

    # Clave foranea de la tabla Role
    role_id = Column(BigInteger, ForeignKey("role.roleId"))

    # Clave foranea de la tabla User
    user_id = Column(BigInteger, ForeignKey("user.id"))

    # Esta relacion pertenece al Role de muchos a uno
    role = relationship("Role", back_populates="user_roles")

    # Esta relacion pertenece al User de muchos a uno
    user = relationship("User", back_populates="roles")