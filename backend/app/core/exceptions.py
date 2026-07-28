from typing import Any, Dict, Optional

class AegisException(Exception):
    """Base exception for AegisOps platform."""
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_SERVER_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}

class ValidationError(AegisException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="VALIDATION_ERROR", status_code=422, details=details)

class AuthenticationError(AegisException):
    def __init__(self, message: str = "Invalid credentials or authorization header") -> None:
        super().__init__(message, code="AUTHENTICATION_FAILED", status_code=401)

class TokenExpiredError(AuthenticationError):
    def __init__(self, message: str = "Authorization token has expired") -> None:
        super().__init__(message, code="TOKEN_EXPIRED", status_code=401)

class PermissionDeniedError(AegisException):
    def __init__(self, message: str = "Permission denied for this resource") -> None:
        super().__init__(message, code="PERMISSION_DENIED", status_code=403)

class ResourceNotFoundError(AegisException):
    def __init__(self, resource_type: str, resource_id: str) -> None:
        message = f"Resource {resource_type} with identity '{resource_id}' was not found."
        super().__init__(
            message,
            code="RESOURCE_NOT_FOUND",
            status_code=404,
            details={"resource_type": resource_type, "resource_id": resource_id}
        )

class DatabaseConnectionError(AegisException):
    def __init__(self, message: str = "Database connection failure") -> None:
        super().__init__(message, code="DATABASE_CONNECTION_ERROR", status_code=503)

class RedisConnectionError(AegisException):
    def __init__(self, message: str = "Redis connection failure") -> None:
        super().__init__(message, code="REDIS_CONNECTION_ERROR", status_code=503)

class AIProviderError(AegisException):
    def __init__(
        self,
        message: str,
        provider: str,
        code: str = "AI_PROVIDER_ERROR",
        status_code: int = 502,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        details = details or {}
        details["provider"] = provider
        super().__init__(message, code=code, status_code=status_code, details=details)

class AIRateLimitError(AIProviderError):
    def __init__(self, provider: str, message: str = "AI Provider rate limits exceeded") -> None:
        super().__init__(message, provider=provider, code="AI_RATE_LIMIT", status_code=429)

class AIConnectionTimeout(AIProviderError):
    def __init__(self, provider: str, message: str = "AI Provider connection timed out") -> None:
        super().__init__(message, provider=provider, code="AI_TIMEOUT", status_code=504)
