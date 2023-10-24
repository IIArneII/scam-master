from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from scam_master.controllers.models.error import Error
from scam_master.services.models.errors import NotFoundError, BadRequestError


def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=Error(message=str(exc)).model_dump(),
    )

def bad_request_handler(request: Request, exc: BadRequestError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=Error(message=str(exc)).model_dump(),
    )

def internal_server_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content='Internal Server Error',
    )

def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=Error(message=str(exc.detail)).model_dump(),
    )
