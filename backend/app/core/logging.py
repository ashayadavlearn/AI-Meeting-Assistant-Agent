"""Structured logging setup with request ID tracing context."""

import logging
import sys
from contextvars import ContextVar

# Context variable holding the unique request ID for the current async task
request_id_ctx: ContextVar[str | None] = ContextVar("request_id_ctx", default=None)


class RequestIdFilter(logging.Filter):
    """Logging filter that injects the current request_id from ContextVar into each log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get() or "-"
        return True


class StructuredFormatter(logging.Formatter):
    """Formats log records with timestamp, level, request_id, logger name, and message."""

    def __init__(self) -> None:
        log_fmt = (
            "[%(asctime)s] [%(levelname)s] [req_id:%(request_id)s] "
            "[%(name)s:%(funcName)s:%(lineno)d] - %(message)s"
        )
        super().__init__(
            fmt=log_fmt,
            datefmt="%Y-%m-%d %H:%M:%S",
        )


def setup_logging(log_level: str = "INFO") -> None:
    """Configures application-wide logging with request ID tracing."""
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Configure root handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.addFilter(RequestIdFilter())
    handler.setFormatter(StructuredFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]

    # Align uvicorn and app loggers
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logger = logging.getLogger(logger_name)
        logger.handlers = [handler]
        logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Retrieves a logger configured with request ID context."""
    return logging.getLogger(name)
