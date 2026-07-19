from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column



from app.core.base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    available_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    tax_percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )