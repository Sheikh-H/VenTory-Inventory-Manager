from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from database.db import database


class Business(database.Model):
    __tablename__ = "business_table"
    business_id: Mapped[int] = mapped_column(primary_key=True)
    business_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String(), nullable=False)
    telephone: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String(), unique=False, nullable=True)
    daily_password: Mapped[str] = mapped_column(
        String(10), unique=False, nullable=False
    )
    created: Mapped[str] = mapped_column(String(20), nullable=False)
    updated: Mapped[str] = mapped_column(String(20), nullable=True)
    employees: Mapped[list["User"]] = relationship(back_populates="business")
    logs: Mapped[list["Log"]] = relationship(back_populates="business")
