from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from database.db import database


class Business(database.Model):
    __tablename__ = "business_table"
    business_id: Mapped[int] = mapped_column(primary_key=True)
    business_name: Mapped[str] = mapped_column(String(), unique=True)
    address: Mapped[str] = mapped_column(String())
    created: Mapped[str] = mapped_column(String())
