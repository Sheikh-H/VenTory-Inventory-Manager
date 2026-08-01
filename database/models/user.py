from database.db import database
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean


class User(database.Model):
    __tablename__ = "user_table"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(
        ForeignKey("business_table.business_id"), nullable=False
    )
    username: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created: Mapped[str] = mapped_column(String(20), nullable=False)
    updated: Mapped[str] = mapped_column(String(20), nullable=True)
    business: Mapped["Business"] = relationship(back_populates="employees")
    logs: Mapped[list["Log"]] = relationship(back_populates="user")
