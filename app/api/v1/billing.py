from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_billing_service
from app.schemas.billing import (
    BillingRequest,
    BillingResponse,
)
from app.services.billing_service import BillingService

BillingServiceDep = Annotated[
    BillingService,
    Depends(get_billing_service),
]

router = APIRouter(
    prefix="/billing",
    tags=["Billing"],
)

@router.post(
    "",
    response_model=BillingResponse,
    status_code=201,
)
def generate_bill(
    request: BillingRequest,
    service: BillingServiceDep,
):
    return service.generate_bill(request)

@router.get(
    "/history/{email}",
)
def purchase_history(
    email: str,
    service: BillingServiceDep,
):
    return service.get_purchase_history(
        email
    )

@router.get(
    "/{bill_id}",
)
def bill_details(
    bill_id: int,
    service: BillingServiceDep,
):
    return service.get_bill(
        bill_id
    )