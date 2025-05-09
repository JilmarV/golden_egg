from sqlalchemy import Table, Column, Integer, ForeignKey
from db.database import Base

user_role = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role.id"), primary_key=True),
)
