from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import database


class Stock(database.Model):
    __tablename__ = "stock_table"
    stock_id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(
        ForeignKey("business_table.business_id"), nullable=False
    )
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=Decimal("0.00")
    )
    supplier: Mapped[str | None] = mapped_column(String(255), nullable=True)

    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    returned: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    damaged: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    total: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    available: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)

    updated: Mapped[str | None] = mapped_column(String(23), nullable=True)
    created: Mapped[str] = mapped_column(String(23), nullable=False)

    business: Mapped["Business"] = relationship(back_populates="stock")
