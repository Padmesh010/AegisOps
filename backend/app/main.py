import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import get_settings
from app.core.exceptions import AegisException
from app.infrastructure.logging import setup_logging
from app.infrastructure.middleware import setup_middlewares
from app.infrastructure.redis import redis_manager
from app.api.v1.router import api_router

# 1. Setup structured logging
setup_logging()
logger = logging.getLogger("app.main")
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle startup and shutdown operations manager."""
    logger.info("Starting up AegisOps Backend Core Services...")
    # Initialize Redis connection
    redis_manager.connect()
    yield
    logger.info("Shutting down AegisOps Backend Core Services...")
    # Disconnect Redis connection pool
    await redis_manager.disconnect()

# 2. Instantiate application
app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 3. Setup middlewares
setup_middlewares(app)

# 4. Standard Exception handling override
@app.exception_handler(AegisException)
async def aegis_exception_handler(request: Request, exc: AegisException) -> JSONResponse:
    logger.error(f"Domain exception intercepted: {exc.message} - Code: {exc.code} - Status: {exc.status_code}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"Unhandled system exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected internal server error occurred."
            }
        }
    )

# 5. Register routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# 6. Serve Frontend Static Assets
from fastapi.staticfiles import StaticFiles
import os
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
