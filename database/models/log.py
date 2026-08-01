from database.db import database
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean


class Log(database.Model):
    __tablename__ = "log_table"
    log_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_table.user_id"), nullable=False
    )
    business_id: Mapped[int] = mapped_column(
        ForeignKey("business_table.business_id"), nullable=False
    )
    timestamp: Mapped[str] = mapped_column(String(), nullable=False)
    comment: Mapped[str] = mapped_column(String(), nullable=False)
    business: Mapped["Business"] = relationship(back_populates="logs")
    user: Mapped["User"] = relationship(back_populates="logs")
