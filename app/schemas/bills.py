from pydantic import BaseModel,EmailStr
from decimal import Decimal



class BillItemRequest(BaseModel):
    product_id: str
    quantity: int

class DenominationRequest(BaseModel):
    denomination: int
    count: int


class BillingRequest(BaseModel):
    email: EmailStr
    cash_paid: Decimal

    items: list[BillItemRequest]

    denominations: list[DenominationRequest]

class BillItemResponse(BaseModel):
    product_name: str

    quantity: int

    unit_price: Decimal

    tax_percentage: Decimal

    tax_amount: Decimal

    line_total: Decimal

class ChangeDenomination(BaseModel):
    denomination: int

    count: int

class BillingResponse(BaseModel):

    customer_email: EmailStr

    items: list[BillItemResponse]

    subtotal: Decimal

    tax_amount: Decimal

    grand_total: Decimal

    cash_paid: Decimal

    balance_amount: Decimal

    denominations: list[ChangeDenomination]