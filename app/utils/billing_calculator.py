from decimal import Decimal

from app.models.product import Product
from app.schemas.billing import (
    BillItemRequest,
    BillTotals,
    BillLine,
)

class BillingCalculator:

    @staticmethod
    def calculate_line(
        product: Product,
        quantity: int,
    ) -> dict:

        subtotal = product.price * quantity

        tax_amount = (
            subtotal * product.tax_percentage
        ) / Decimal("100")

        total = subtotal + tax_amount

        return BillLine(
    product_id=product.product_id,
    quantity=quantity,
    unit_price=product.price,
    tax_percentage=product.tax_percentage,
    subtotal=subtotal,
    tax_amount=tax_amount,
    total=total,
)
    @staticmethod
    def calculate_totals(
        products: dict[str, Product],
        items: list[BillItemRequest],
    ) -> BillTotals:

        subtotal = Decimal("0.00")
        tax_amount = Decimal("0.00")

        for item in items:

            product = products[item.product_id]

            line = BillingCalculator.calculate_line(
                product=product,
                quantity=item.quantity,
            )

            subtotal += line.subtotal
            tax_amount += line.tax_amount

        return BillTotals(
            subtotal=subtotal,
            tax_amount=tax_amount,
            grand_total=subtotal + tax_amount,
        )