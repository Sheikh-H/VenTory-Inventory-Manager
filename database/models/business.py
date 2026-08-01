from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, null
from database.db import database


class Business(database.Model):
    __tablename__ = "business_table"
    
    business_id: Mapped[int] = mapped_column(primary_key=True)
    
    business_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    address: Mapped[str] = mapped_column(String(), nullable=False)
    
    telephone: Mapped[str] = mapped_column(String(15), nullable=False)
    
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    
    logo_url: Mapped[str | None] = mapped_column(String(), unique=True, nullable=True)
    
    daily_password: Mapped[str] = mapped_column(String(), unique=False, nullable=False)
    
    created: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc).replace(microsecond=0), nullable = False)
    
    
    employees: [list('User')] = relationship(
        back_populates='User'
    )
    logs: [list()] - relationship(
        back_populates=
    )
