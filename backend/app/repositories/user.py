from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.auth import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """UserRepository subclassing BaseRepository for the User model."""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> User | None:
        """Find a user by email, scoped to the current tenant context."""
        query = select(self.model).filter(self.model.email == email)
        query = self._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return result.scalars().first()
