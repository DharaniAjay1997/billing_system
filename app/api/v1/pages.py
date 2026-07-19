from fastapi import APIRouter, Request

from app.core.template import templates
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=["Pages"],
)

templates = Jinja2Templates(
    directory="app/templates"
)

@router.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
        },
    )

@router.get("/billing")
def billing_page(
    request: Request,
):

    return templates.TemplateResponse(
        "billing.html",
        {
            "request": request,
        },
    )

@router.get("/history/")
def purchase_history(
    request: Request,
):
    return templates.TemplateResponse(
        "purchase_history.html",
        {
            "request": request,
        },
    )

@router.get("/invoice/{bill_id}")
def invoice_page(
    request: Request,
    bill_id: int,
):
    return templates.TemplateResponse(
        "invoice.html",
        {
            "request": request,
            "bill_id": bill_id,
        },
    )