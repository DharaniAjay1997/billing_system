from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.api.v1.pages import router as pages_router
from app.core.handlers import register_exception_handlers



app = FastAPI(title="Billing System")

register_exception_handlers(app)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

# HTML pages
app.include_router(pages_router)

# REST APIs
app.include_router(api_router)