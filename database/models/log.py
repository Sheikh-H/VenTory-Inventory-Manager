from database.db import database
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean


class Log(database.Model):
    __tablename__ = "logs_table"
    log_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey=True)
    business_id: Mapped[int] = mapped_column(ForeignKey=True)
    date: Mapped[str] = mapped_column(String())
    time: Mapped[str] = mapped_column(String())
    comment: Mapped[str] = mapped_column(String())
