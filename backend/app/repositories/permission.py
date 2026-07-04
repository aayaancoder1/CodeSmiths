from typing import List
from uuid import UUID
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.auth import user_groups
from app.models.permission import Permission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    """PermissionRepository subclassing BaseRepository for ACL mappings."""

    def __init__(self, db: AsyncSession):
        super().__init__(Permission, db)

    async def get_acl_for_document(self, document_id: UUID) -> List[Permission]:
        """Retrieve all ACL permissions associated with a specific document."""
        query = select(Permission).filter(Permission.document_id == document_id)
        query = self._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_user_group_ids(self, user_id: UUID) -> List[UUID]:
        """Fetch all group UUIDs that a specific user belongs to."""
        query = select(user_groups.c.group_id).filter(user_groups.c.user_id == user_id)
        result = await self.db.execute(query)
        return [row[0] for row in result.all()]

    async def get_matching_permissions(
        self, user_id: UUID, group_ids: List[UUID], document_id: UUID
    ) -> List[Permission]:
        """Retrieve all ACL rules matching a user (directly or via group memberships)."""
        query = select(Permission).filter(
            Permission.document_id == document_id,
            or_(
                Permission.user_id == user_id,
                Permission.group_id.in_(group_ids) if group_ids else False
            )
        )
        query = self._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return list(result.scalars().all())
