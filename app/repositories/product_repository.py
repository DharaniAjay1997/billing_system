from sqlalchemy import select

from app.models.product import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository):

    def get_by_product_ids(
        self,
        product_ids: list[str],
    ) -> dict[str, Product]:

        statement = (
            select(Product)
            .where(Product.product_id.in_(product_ids))
        )

        products = self.db.scalars(statement).all()

        return {
            product.product_id: product
            for product in products
        }

    def update_stock(
        self,
        products: dict[str, Product],
        items,
    ) -> None:

        for item in items:

            product = products[item.product_id]

            product.available_stock -= item.quantity