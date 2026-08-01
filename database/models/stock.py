from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, REAL
from database.db import database


class Stock(database.Model):
    __tablename__ = "stock_table"
    stock_id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("business_table.business_id"))
    description: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    price: Mapped[int] = mapped_column(REAL(), nullable=False, default=0.00)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    updated: Mapped[str] = mapped_column(String(20), nullable=True)
    created: Mapped[str] = mapped_column(String(20), nullable=False)
