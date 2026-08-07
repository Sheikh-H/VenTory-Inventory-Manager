from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import database


class Log(database.Model):
    __tablename__ = "log_table"
    log_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_table.user_id"), nullable=False
    )
    business_id: Mapped[int] = mapped_column(
        ForeignKey("business_table.business_id"), nullable=False
    )
    timestamp: Mapped[str] = mapped_column(String(19), nullable=False)
    comment: Mapped[str] = mapped_column(String(), nullable=False)
    business: Mapped["Business"] = relationship(back_populates="logs")
