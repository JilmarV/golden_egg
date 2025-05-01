from sqlalchemy import Table, Column, Integer, ForeignKey
from db.database import Base

orders_eggs = Table(
    "orders_eggs",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("egg_id", Integer, ForeignKey("egg.id"), primary_key=True),
)