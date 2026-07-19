from app.models.bill import Bill
from app.models.bill_items import BillItem
from app.repositories.base_repository import BaseRepository
from app.utils.invoice_generator import InvoiceGenerator
from sqlalchemy.orm import joinedload

from sqlalchemy import select



class BillingRepository(BaseRepository):

    def create_bill(
        self,
        customer_id: int,
        subtotal,
        tax_amount,
        grand_total,
        cash_paid,
        balance_amount,
    ) -> Bill:

        bill = Bill(
            invoice_number=InvoiceGenerator.generate(),
            customer_id=customer_id,
            subtotal=subtotal,
            tax_amount=tax_amount,
            grand_total=grand_total,
            cash_paid=cash_paid,
            balance_amount=balance_amount,
        )

        self.add(bill)
        self.flush()

        return bill

    def create_bill_items(
        self,
        bill_items: list[BillItem],
    ) -> None:

        self.db.add_all(bill_items)
        self.flush()



    def get_customer_bills(
        self,
        customer_id: int,
    ):

        statement = (
            select(Bill)
            .where(
                Bill.customer_id == customer_id
            )
            .order_by(
                Bill.created_at.desc()
            )
        )

        return self.db.scalars(statement).all()
    
    def get_bill(
        self,
        bill_id: int,
    ):

        statement = (
            select(Bill)
            .options(
                joinedload(Bill.customer),
                joinedload(Bill.items).joinedload(BillItem.product),
            )
            .where(
                Bill.id == bill_id
            )
        )

        return self.db.scalar(statement)

    # def get_bill(
    #     self,
    #     bill_id: int,
    # ):

    #     statement = (
    #         select(Bill)
    #         .where(
    #             Bill.id == bill_id
    #         )
    #     )

    #     return self.db.scalar(statement)