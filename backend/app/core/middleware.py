"""Custom HTTP middleware for Request ID tracing and access logging."""

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import request_id_ctx

logger = logging.getLogger("app.access")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Intercepts requests to assign a unique X-Request-ID and log request lifecycle."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        token = request_id_ctx.set(req_id)

        request.state.request_id = req_id

        start_time = time.perf_counter()
        client_host = request.client.host if request.client else "unknown"

        logger.info(
            "--> %s %s from %s",
            request.method,
            request.url.path,
            client_host,
        )

        try:
            response = await call_next(request)
            process_time_ms = (time.perf_counter() - start_time) * 1000
            response.headers["X-Request-ID"] = req_id
            response.headers["X-Response-Time"] = f"{process_time_ms:.2f}ms"

            logger.info(
                "<-- %s %s %d (%.2fms)",
                request.method,
                request.url.path,
                response.status_code,
                process_time_ms,
            )
            return response
        except Exception as exc:
            process_time_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "<-- ERROR %s %s (%.2fms)",
                request.method,
                request.url.path,
                process_time_ms,
            )
            from app.core.handlers import unhandled_exception_handler

            response = await unhandled_exception_handler(request, exc)
            response.headers["X-Request-ID"] = req_id
            response.headers["X-Response-Time"] = f"{process_time_ms:.2f}ms"
            return response
        finally:
            request_id_ctx.reset(token)
