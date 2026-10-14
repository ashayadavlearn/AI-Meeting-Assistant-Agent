"""Global exception handlers ensuring uniform error envelopes across all responses."""

import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import Settings, get_settings
from app.core.exceptions import AppException
from app.schemas.common import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


def create_error_response(
    status_code: int,
    code: str,
    message: str,
    details: object = None,
) -> JSONResponse:
    """Helper to build a uniform JSONResponse containing an ErrorResponse envelope."""
    payload = ErrorResponse(
        error=ErrorDetail(
            code=code,
            message=message,
            details=details,
        )
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump())


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handles all domain and application-specific exceptions."""
    logger.warning(
        "Application exception: code=%s, status=%d, message=%s, path=%s",
        exc.code,
        exc.status_code,
        exc.message,
        request.url.path,
    )
    return create_error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handles FastAPI/Pydantic request validation errors."""
    logger.warning(
        "Validation error on path=%s: %s",
        request.url.path,
        exc.errors(),
    )
    formatted_errors = []
    for err in exc.errors():
        loc = " -> ".join(str(item) for item in err.get("loc", []))
        formatted_errors.append(
            {
                "field": loc,
                "message": err.get("msg", "Invalid value"),
                "type": err.get("type", "value_error"),
            }
        )

    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="VALIDATION_ERROR",
        message="Request payload or parameter validation failed.",
        details=formatted_errors,
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handles standard Starlette/FastAPI HTTPExceptions."""
    logger.warning(
        "HTTPException on path=%s: status=%d, detail=%s",
        request.url.path,
        exc.status_code,
        exc.detail,
    )
    status_to_code = {
        status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
        status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
        status.HTTP_403_FORBIDDEN: "FORBIDDEN",
        status.HTTP_404_NOT_FOUND: "NOT_FOUND",
        status.HTTP_409_CONFLICT: "CONFLICT",
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: "PAYLOAD_TOO_LARGE",
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: "UNSUPPORTED_MEDIA_TYPE",
        status.HTTP_422_UNPROCESSABLE_ENTITY: "UNPROCESSABLE_ENTITY",
        status.HTTP_429_TOO_MANY_REQUESTS: "RATE_LIMIT_EXCEEDED",
    }
    code = status_to_code.get(exc.status_code, "HTTP_ERROR")
    return create_error_response(
        status_code=exc.status_code,
        code=code,
        message=str(exc.detail),
        details=getattr(exc, "headers", None),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback handler for unhandled exceptions (HTTP 500) preventing sensitive leakage."""
    logger.exception(
        "Unhandled server error on path=%s: %s",
        request.url.path,
        str(exc),
    )
    settings: Settings = getattr(request.app.state, "settings", None) or get_settings()
    details = str(exc) if settings.DEBUG or settings.ENVIRONMENT == "development" else None

    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected server error occurred. Please try again later.",
        details=details,
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Registers all global exception handlers to the FastAPI app instance."""
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)
