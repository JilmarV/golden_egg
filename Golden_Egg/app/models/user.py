from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phoneNumber = Column(String)
    user = Column(String, unique=True, index=True)
    password = Column(String)

    # Relación con Order un usuario puede tener muchas ordenes
    # back_populates el relación inversa de Order se llama 'user'
    orders = relationship("Order", back_populates="user")