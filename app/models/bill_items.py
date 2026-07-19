from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import BaseModel


class BillItem(BaseModel):
    __tablename__ = "bill_items"

    bill_id: Mapped[int] = mapped_column(
        ForeignKey("bills.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    tax_percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    bill: Mapped["Bill"] = relationship(
        back_populates="items",
    )

    product: Mapped["Product"] = relationship()

    def __repr__(self) -> str:
        return (
            f"<BillItem("
            f"bill_id={self.bill_id}, "
            f"product_id={self.product_id}, "
            f"qty={self.quantity})>"
        )