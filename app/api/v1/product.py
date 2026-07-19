from fastapi import APIRouter, Depends

from app.api.deps import get_product_service
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
# from app.services.product_service import ProductService
# from typing import Annotated

# from fastapi import Depends
# from sqlalchemy.orm import Session
# from app.db.session import get_db

from app.api.deps import ProductServiceDep
from http import HTTPStatus

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.post(
    "",
    response_model=ProductResponse,
    status_code=HTTPStatus.CREATED,
)
def create_product(
    product: ProductCreate,
    service: ProductServiceDep
):
    return service.create_product(product)

@router.get(
    "",
    response_model=list[ProductResponse],
)
def list_products(
    service: ProductServiceDep
):
    return service.list_products()

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    service: ProductServiceDep
):
    return service.get_product_by_id(product_id)

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    service: ProductServiceDep,
):
    return service.update_product(
        product_id,
        product,
    )

from fastapi import Response


@router.delete(
    "/{product_id}",
    status_code=HTTPStatus.NO_CONTENT
)
def delete_product(
    product_id: int,
    service: ProductServiceDep,
):
    service.delete_product(product_id)

    return Response(status_code=204)