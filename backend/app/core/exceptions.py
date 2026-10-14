"""Application-wide custom exception hierarchy with uniform error code mappings."""

from typing import Any


class AppException(Exception):
    """Base application exception for all domain and service errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details


class EntityNotFoundException(AppException):
    """Raised when a requested resource or entity cannot be found."""

    def __init__(
        self,
        entity_name: str,
        entity_id: Any,
        message: str | None = None,
    ) -> None:
        msg = message or f"{entity_name} with identifier '{entity_id}' was not found."
        super().__init__(
            message=msg,
            code="NOT_FOUND",
            status_code=404,
            details={"entity": entity_name, "id": str(entity_id)},
        )


class UnauthorizedException(AppException):
    """Raised when authentication credentials are missing or invalid."""

    def __init__(self, message: str = "Authentication required or credentials invalid.") -> None:
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
        )


class ForbiddenException(AppException):
    """Raised when an authenticated user does not have access to a resource."""

    def __init__(
        self,
        message: str = "You do not have permission to access this resource.",
    ) -> None:
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=403,
        )


class ConflictException(AppException):
    """Raised when a unique constraint or conflicting state prevents the operation."""

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=409,
            details=details,
        )


class ValidationException(AppException):
    """Raised when domain or business rule validation fails."""

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class PayloadTooLargeException(AppException):
    """Raised when an uploaded file or payload exceeds size limits."""

    def __init__(self, message: str = "Payload exceeds maximum allowed size.") -> None:
        super().__init__(
            message=message,
            code="PAYLOAD_TOO_LARGE",
            status_code=413,
        )


class UnsupportedMediaTypeException(AppException):
    """Raised when an uploaded file has an unsupported MIME or extension type."""

    def __init__(self, message: str = "Unsupported media type.") -> None:
        super().__init__(
            message=message,
            code="UNSUPPORTED_MEDIA_TYPE",
            status_code=415,
        )


class RateLimitException(AppException):
    """Raised when a client exceeds the allowed request rate."""

    def __init__(self, message: str = "Rate limit exceeded. Please try again later.") -> None:
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            status_code=429,
        )


class InternalServerException(AppException):
    """Raised when an unexpected internal error occurs."""

    def __init__(self, message: str = "An unexpected server error occurred.") -> None:
        super().__init__(
            message=message,
            code="INTERNAL_SERVER_ERROR",
            status_code=500,
        )
