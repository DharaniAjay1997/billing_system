from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    product_id: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)
    available_stock: int = Field(..., ge=0)
    price: Decimal = Field(..., gt=0)
    tax_percentage: Decimal = Field(..., ge=0)


class ProductUpdate(BaseModel):
    product_id: str | None = Field(default=None, max_length=20)
    name: str | None = Field(default=None, max_length=100)
    available_stock: int | None = Field(default=None, ge=0)
    price: Decimal | None = Field(default=None, gt=0)
    tax_percentage: Decimal | None = Field(default=None, ge=0)


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: str
    name: str
    available_stock: int
    price: Decimal
    tax_percentage: Decimal
    created_at: datetime
    updated_at: datetime