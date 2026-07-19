from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import BaseModel


class Customer(BaseModel):
    __tablename__ = "customers"


    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    bills: Mapped[list["Bill"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Customer(id={self.name}, email='{self.email}')>"