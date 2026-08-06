from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import database


class User(database.Model):
    __tablename__ = "user_table"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(
        ForeignKey("business_table.business_id"), nullable=False
    )
    username: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(3), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(8), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created: Mapped[str] = mapped_column(String(19), nullable=False)
    updated: Mapped[str | None] = mapped_column(String(19), nullable=True)
    password_reset: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    business: Mapped["Business"] = relationship(back_populates="employees")
    logs: Mapped[list["Log"]] = relationship(back_populates="user")
