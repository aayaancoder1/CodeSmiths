import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import settings
from app.core.exceptions import (
    BrainException,
    EntityNotFoundError,
    PermissionDeniedError,
    TenantIsolationError,
    ValidationError,
    ConnectorError,
    ParserError,
    EventPublishError,
)
from app.api.health import router as health_router
from app.api.documents import router as documents_router
from app.api.connectors import router as connectors_router
from app.api.permissions import router as permissions_router
from app.api.audit import router as audit_router
from app.api.jobs import router as jobs_router
from app.api.ask import router as ask_router
from app.middleware.tenant import RequestContextMiddleware

# Configure basic logging formatting suited for enterprise debugging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Knowledge Engine API supporting multi-tenant document ingestion, chunking, and permission checks.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware for frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request context middleware
app.add_middleware(RequestContextMiddleware)


# Centralized Exception Handlers
@app.exception_handler(PermissionDeniedError)
async def permission_denied_exception_handler(request: Request, exc: PermissionDeniedError):
    logger.warning(f"PermissionDeniedError: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"code": exc.code, "message": exc.message, "details": exc.details},
    )


@app.exception_handler(EntityNotFoundError)
async def entity_not_found_exception_handler(request: Request, exc: EntityNotFoundError):
    logger.info(f"EntityNotFoundError: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"code": exc.code, "message": exc.message, "details": exc.details},
    )


@app.exception_handler(TenantIsolationError)
async def tenant_isolation_exception_handler(request: Request, exc: TenantIsolationError):
    logger.critical(f"TenantIsolationError: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": exc.code, "message": exc.message, "details": exc.details},
    )


@app.exception_handler(ValidationError)
@app.exception_handler(ConnectorError)
@app.exception_handler(ParserError)
async def client_side_brain_exception_handler(request: Request, exc: BrainException):
    logger.error(f"ClientError ({exc.__class__.__name__}): {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": exc.code, "message": exc.message, "details": exc.details},
    )


@app.exception_handler(EventPublishError)
async def server_side_brain_exception_handler(request: Request, exc: BrainException):
    logger.error(f"ServerError ({exc.__class__.__name__}): {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"code": exc.code, "message": exc.message, "details": exc.details},
    )


@app.exception_handler(BrainException)
async def generic_brain_exception_handler(request: Request, exc: BrainException):
    logger.error(f"BrainException: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"code": exc.code, "message": exc.message, "details": exc.details},
    )


# Register API Routers
app.include_router(health_router)
app.include_router(documents_router)
app.include_router(connectors_router)
app.include_router(permissions_router)
app.include_router(audit_router)
app.include_router(jobs_router)
app.include_router(ask_router)
