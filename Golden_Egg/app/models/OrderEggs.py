from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base

class OrderEggs(Base):
    __tablename__ = "order_eggs"

    id = Column(BigInteger, primary_key=True, index=True)

    # Clave foranea de la tabla Role
    order_id = Column(BigInteger, ForeignKey("order.orderId"))

    # Clave foranea de la tabla User
    egg_id = Column(BigInteger, ForeignKey("egg.id"))

    # Esta relacion pertenece al Role de muchos a uno
    order = relationship("Order", back_populates="order")

    # Esta relacion pertenece al User de muchos a uno
    egg = relationship("Egg", back_populates="egg")