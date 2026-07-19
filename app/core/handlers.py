from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    DuplicateResourceException,
    ResourceNotFoundException,
    ValidationException,
)

async def resource_not_found_handler(
    request: Request,
    exc: ResourceNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )

async def duplicate_resource_handler(
    request: Request,
    exc: DuplicateResourceException,
):
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": exc.message,
        },
    )

async def validation_exception_handler(
    request: Request,
    exc: ValidationException,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message,
        },
    )


def register_exception_handlers(
    app: FastAPI,
):

    app.add_exception_handler(
        ResourceNotFoundException,
        resource_not_found_handler,
    )

    app.add_exception_handler(
        DuplicateResourceException,
        duplicate_resource_handler,
    )

    app.add_exception_handler(
        ValidationException,
        validation_exception_handler,
    )