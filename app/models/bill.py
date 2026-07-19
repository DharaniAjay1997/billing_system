from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric,String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.core.base import BaseModel


class Bill(BaseModel):
    __tablename__ = "bills"

    invoice_number: Mapped[str] = mapped_column(
    String(30),
    unique=True,
    nullable=False,
)
    
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    cash_paid: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    balance_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="bills",
    )

    items: Mapped[list["BillItem"]] = relationship(
        back_populates="bill",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Bill(id={self.id}, total={self.grand_total})>"