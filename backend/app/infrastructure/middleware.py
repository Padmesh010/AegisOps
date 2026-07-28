import logging
import time
import uuid
from contextvars import ContextVar
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from app.core.config import get_settings

logger = logging.getLogger("app.middleware")
settings = get_settings()

# ContextVar to store correlation ID for log injection
correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id", default="")

class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        corr_id = request.headers.get("X-Correlation-ID")
        if not corr_id:
            corr_id = str(uuid.uuid4())
            
        token = correlation_id_ctx.set(corr_id)
        
        # Inject correlation_id to log filters globally
        class CorrelationFilter(logging.Filter):
            def filter(self, record: logging.LogRecord) -> bool:
                record.correlation_id = corr_id  # type: ignore
                return True
                
        logging.getLogger().addFilter(CorrelationFilter())

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = corr_id
        correlation_id_ctx.reset(token)
        return response

class LoggingAndMetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()
        method = request.method
        url = str(request.url.path)
        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            f"Incoming request: {method} {url}",
            extra={"extra_fields": {"client_ip": client_ip, "method": method, "url": url}}
        )

        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            duration_ms = int(process_time * 1000)
            
            logger.info(
                f"Request completed: {method} {url} - Status: {response.status_code} - Duration: {duration_ms}ms",
                extra={
                    "extra_fields": {
                        "status_code": response.status_code,
                        "duration_ms": duration_ms,
                        "method": method,
                        "url": url,
                    }
                }
            )
            response.headers["X-Process-Time-Ms"] = str(duration_ms)
            return response
            
        except Exception as exc:
            process_time = time.perf_counter() - start_time
            duration_ms = int(process_time * 1000)
            logger.exception(
                f"Request failed: {method} {url} - Error: {str(exc)} - Duration: {duration_ms}ms",
                extra={
                    "extra_fields": {
                        "status_code": 500,
                        "duration_ms": duration_ms,
                        "method": method,
                        "url": url,
                    }
                }
            )
            raise exc

def setup_middlewares(app: FastAPI) -> None:
    # 1. CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. GZip
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # 3. Correlation ID
    app.add_middleware(CorrelationIDMiddleware)

    # 4. Request Logging & Metrics
    app.add_middleware(LoggingAndMetricsMiddleware)
