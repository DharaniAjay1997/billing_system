from sqlalchemy import select

from app.core.exceptions import (
    DuplicateResourceException,
    ResourceNotFoundException,
)
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.base_service import BaseService


class ProductService(BaseService):

    def create_product(self, product: ProductCreate) -> Product:
        if self._get_product_by_product_id(product.product_id):
            raise DuplicateResourceException(
                "Product ID already exists."
            )

        db_product = Product(**product.model_dump())

        self.add(db_product)
        self.commit()
        self.refresh(db_product)

        return db_product

    def list_products(self) -> list[Product]:
        statement = select(Product)

        return list(self.db.scalars(statement).all())

    def get_product_by_id(self, product_id: int) -> Product:
        product = self._get_product_by_id(product_id)

        if product is None:
            raise ResourceNotFoundException(
                f"Product with id '{product_id}' not found."
            )

        return product

    def update_product(
        self,
        product_id: int,
        product: ProductUpdate,
    ) -> Product:

        db_product = self.get_product_by_id(product_id)

        update_data = product.model_dump(exclude_unset=True)

        # Product ID should never change
        update_data.pop("product_id", None)

        for field, value in update_data.items():
            setattr(db_product, field, value)

        self.commit()
        self.refresh(db_product)

        return db_product

    def delete_product(self, product_id: int) -> None:
        db_product = self.get_product_by_id(product_id)

        self.delete(db_product)
        self.commit()

    # ------------------------------------------------------------------
    # Private Helper Methods
    # ------------------------------------------------------------------

    def _get_product_by_id(self, product_id: int) -> Product | None:
        statement = (
            select(Product)
            .where(Product.id == product_id)
        )

        return self.db.scalar(statement)

    def _get_product_by_product_id(
        self,
        product_id: str,
    ) -> Product | None:
        statement = (
            select(Product)
            .where(Product.product_id == product_id)
        )

        return self.db.scalar(statement)