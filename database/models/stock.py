from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from database.db import database


class Stock(database.Model):
    __tablename__ = "stock_table"
    stock_id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey=True)
    description: Mapped[str] = mapped_column(String(), unique=True)
    quantity: Mapped[int] = mapped_column(Integer())
    image_url: Mapped[str] = mapped_column(String())
    updated: Mapped[str] = mapped_column(String())
    created: Mapped[str] = mapped_column(String())
