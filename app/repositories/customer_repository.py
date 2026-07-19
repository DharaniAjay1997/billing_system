from sqlalchemy import select

from app.models.customer import Customer
from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):

    def get_by_email(
        self,
        email: str,
    ) -> Customer | None:

        statement = (
            select(Customer)
            .where(Customer.email == email)
        )

        return self.db.scalar(statement)

    def create(
        self,
        email: str,
    ) -> Customer:

        customer = Customer(
            email=email,
        )

        self.add(customer)
        self.flush()

        return customer