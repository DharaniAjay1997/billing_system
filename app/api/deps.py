from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.billing_service import BillingService
from app.services.product_service import ProductService


def get_product_service(
    db: Annotated[Session, Depends(get_db)],
) -> ProductService:
    return ProductService(db)


def get_billing_service(
    db: Annotated[Session, Depends(get_db)],
) -> BillingService:
    return BillingService(db)


ProductServiceDep = Annotated[
    ProductService,
    Depends(get_product_service),
]

BillingServiceDep = Annotated[
    BillingService,
    Depends(get_billing_service),
]