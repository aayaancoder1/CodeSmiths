from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config.config import settings

# Create async engine with robust connection pooling suited for enterprise traffic
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Automatically verify connections are alive before using them
    pool_size=20,        # Maximum number of persistent connections in pool
    max_overflow=10,     # Allow up to 10 additional connections when pool is full
)

# Async session maker bound to engine
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent accessing attributes after commit from raising DetachedInstanceError
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection helper providing a scoped async database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
