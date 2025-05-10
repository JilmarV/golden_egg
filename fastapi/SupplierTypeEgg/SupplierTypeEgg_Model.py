from sqlalchemy import Table, Column, Integer, ForeignKey
from db.database import Base

Supplier_type = Table(
    "supplier_typeEgg",
    Base.metadata,
    Column("supplier_id", Integer, ForeignKey("supplier.id"), primary_key=True),
    Column("type_egg_id", Integer, ForeignKey("type_egg.id"), primary_key=True),
)