from sqlalchemy.orm import Session

from app.repositories.billing_repository import BillingRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.billing import BillingRequest
from app.utils.denomination_calculator import DenominationCalculator

from app.schemas.billing import PurchaseHistoryResponse
from app.core.exceptions import ResourceNotFoundException
from app.core.exceptions import ValidationException
from app.models.bill_items import BillItem
from app.utils.billing_calculator import BillingCalculator

from app.models.customer import Customer

from app.task.email_task import send_invoice_email

from decimal import Decimal

from app.schemas.billing import (
    BillingResponse,
    BillItemResponse,
    ChangeItem,
    BillTotals
)


class BillingService:

    def __init__(self, db: Session):
        self.db = db

        self.customer_repository = CustomerRepository(db)
        self.product_repository = ProductRepository(db)
        self.billing_repository = BillingRepository(db)
    
    def generate_bill(
    self,
    request: BillingRequest,
):

        customer = self._get_or_create_customer(
            request.email,
        )

        products = self._validate_products(
            request.items,
        )

        self._validate_stock(
            products,
            request.items,
        )

        totals = self._calculate_bill(
            products,
            request.items,
        )

        balance = self._calculate_balance(
            grand_total=totals.grand_total,
            cash_paid=request.cash_paid,
        )

        try:
            change = self._calculate_denominations(
            balance=balance,
            available_denominations=request.denominations,
        )
        except ValueError as e:
            raise ValidationException(str(e))

        try:

            bill = self._create_bill(
                customer=customer,
                totals=totals,
                cash_paid=request.cash_paid,
                balance=balance,
            )

            self._create_bill_items(
                bill=bill,
                products=products,
                items=request.items,
            )

            self._update_stock(
                products=products,
                items=request.items,
            )

            self.billing_repository.commit()

            # self._send_email(
            #     bill=bill,
            # )

            send_invoice_email.delay(bill.id)

            return self._build_response(
                bill=bill,
                change=change,
            )

        except Exception:

            self.billing_repository.rollback()
            raise
        

    def _get_or_create_customer(self,email: str,):
        customer = self.customer_repository.get_by_email(email)

        if customer:
            return customer

        return self.customer_repository.create(email)
    


    def _validate_products(self,items,):
        product_ids = [
            item.product_id
            for item in items
        ]

        products = self.product_repository.get_by_product_ids(
            product_ids
        )

        missing_products = (
            set(product_ids)
            - set(products.keys())
        )

        if missing_products:
            raise ResourceNotFoundException(
                f"Products not found: "
                f"{', '.join(missing_products)}"
            )

        return products


    def _validate_stock(self,products,items,):

        for item in items:

            product = products[item.product_id]

            if item.quantity <= 0:

                raise ValidationException(
                    "Quantity must be greater than zero."
                )

            if product.available_stock < item.quantity:

                raise ValidationException(
                    f"Insufficient stock for "
                    f"{product.name}"
                )
            
    def _update_stock(self,products,items,):
        self.product_repository.update_stock(
            products,
            items,
        )

    def _calculate_bill(
    self,
    products,
    items,
):

        return BillingCalculator.calculate_totals(
            products,
            items,
        )
    
    def _calculate_balance(
    self,
    grand_total: Decimal,
    cash_paid: Decimal,
) -> Decimal:

        if cash_paid < grand_total:
            raise ValidationException(
                "Insufficient payment amount."
            )

        return cash_paid - grand_total
    
    def _calculate_denominations(
    self,
    balance,
    available_denominations,
):

        return DenominationCalculator.calculate(
        balance,
        available_denominations,
    )

    def _create_bill(
    self,
    customer: Customer,
    totals: BillTotals,
    cash_paid,
    balance,
):

        return self.billing_repository.create_bill(
        customer_id=customer.id,
        subtotal=totals.subtotal,
        tax_amount=totals.tax_amount,
        grand_total=totals.grand_total,
        cash_paid=cash_paid,
        balance_amount=balance,
    )
        


    def _create_bill_items(
    self,
    bill,
    products,
    items,
):

        bill_items = []

        for item in items:

            product = products[item.product_id]

            line = BillingCalculator.calculate_line(
                product=product,
                quantity=item.quantity,
            )

            bill_items.append(
                BillItem(
                    bill_id=bill.id,
                    product_id=product.id,
                    quantity=line.quantity,
                    unit_price=line.unit_price,
                    tax_percentage=line.tax_percentage,
                    tax_amount=line.tax_amount,
                    line_total=line.total,
                )
            )

        self.billing_repository.create_bill_items(
            bill_items
    
            )
        
    def _build_response(
    self,
    bill,
    change,
):
        items = []

        for item in bill.items:

            items.append(

                BillItemResponse(
                    product_name=item.product.name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    tax_percentage=item.tax_percentage,
                    tax_amount=item.tax_amount,
                    line_total=item.line_total,
                )

            )

        return BillingResponse(

            invoice_number=bill.invoice_number,

            customer_email=bill.customer.email,

            subtotal=bill.subtotal,

            tax_amount=bill.tax_amount,

            grand_total=bill.grand_total,

            cash_paid=bill.cash_paid,

            balance_amount=bill.balance_amount,

            items=items,

            change=[
                ChangeItem(**item)
                for item in change
            ],

            created_at=bill.created_at.isoformat(),
        )
    
    def get_purchase_history(
    self,
    email: str,
):

        customer = self.customer_repository.get_by_email(
            email
        )

        if not customer:

            raise ResourceNotFoundException(
                "Customer not found."
            )

        return self.billing_repository.get_customer_bills(
            customer.id
        )
    
    def get_bill(
    self,
    bill_id: int,
):

        bill = self.billing_repository.get_bill(
            bill_id
        )

        if not bill:

            raise ResourceNotFoundException(
                "Bill not found."
            )

        return bill
    
