from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db_session
from app.events.publisher import RedisEventPublisher

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Liveness check", description="Determine if the application process is running.")
async def health_check():
    """Simple HTTP 200 check confirming the app process is live."""
    return {"status": "healthy"}


@router.get("/ready", summary="Readiness check", description="Verify external dependencies (PostgreSQL and Redis) are responsive.")
async def readiness_check(db: AsyncSession = Depends(get_db_session)):
    """Verifies that the backend can successfully query PostgreSQL and ping Redis."""
    # 1. Test Database connection
    try:
        await db.execute(select(1))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

    # 2. Test Redis connection
    try:
        publisher = RedisEventPublisher()
        client = publisher._get_client()
        client.ping()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Redis connectivity failed: {str(e)}"
        )

    return {"status": "ready"}
