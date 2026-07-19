from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel,EmailStr



class BillLine(BaseModel):
    product_id: str
    quantity: int
    unit_price: Decimal
    tax_percentage: Decimal
    subtotal: Decimal
    tax_amount: Decimal
    total: Decimal

class BillTotals(BaseModel):
    subtotal: Decimal
    tax_amount: Decimal
    grand_total: Decimal


class ChangeItem(BaseModel):
    denomination: int
    count: int


class BillItemResponse(BaseModel):
    product_name: str
    quantity: int
    unit_price: Decimal
    tax_percentage: Decimal
    tax_amount: Decimal
    line_total: Decimal


class BillingResponse(BaseModel):
    invoice_number: str
    customer_email: EmailStr

    subtotal: Decimal
    tax_amount: Decimal
    grand_total: Decimal

    cash_paid: Decimal
    balance_amount: Decimal

    items: list[BillItemResponse]

    change: list[ChangeItem]

    created_at: str

class BillItemRequest(BaseModel):
    product_id: str
    quantity: int


class DenominationRequest(BaseModel):
    denomination: int
    count: int

class BillingRequest(BaseModel):
    email: EmailStr
    items: list[BillItemRequest]
    denominations: list[DenominationRequest]
    cash_paid: Decimal

class PurchaseHistoryResponse(BaseModel):

    bill_id: int

    invoice_number: str

    grand_total: Decimal

    created_at: datetime


class InvoiceResponse(BaseModel):

    invoice_number: str

    customer_email: EmailStr

    subtotal: Decimal

    tax_amount: Decimal

    grand_total: Decimal

    cash_paid: Decimal

    balance_amount: Decimal

    created_at: datetime

    items: list[BillItemResponse]