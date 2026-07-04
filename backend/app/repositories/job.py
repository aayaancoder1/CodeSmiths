from datetime import datetime
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.job import Job, ConnectorSync
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job]):
    """JobRepository subclassing BaseRepository for task management."""

    def __init__(self, db: AsyncSession):
        super().__init__(Job, db)

    async def update_job_status(self, job_id: UUID, status: str, error_message: str | None = None) -> Job | None:
        """Update status and optionally record error message for a background job."""
        job = await self.get(job_id)
        if job:
            update_data = {"status": status}
            if error_message:
                update_data["error_message"] = error_message
            return await self.update(job, update_data)
        return None

    async def get_active_connector_sync(self, connector_type: str) -> ConnectorSync | None:
        """Fetch active/running synchronization record for a specific connector type."""
        query = select(ConnectorSync).filter(
            ConnectorSync.connector_type == connector_type,
            ConnectorSync.status == "syncing"
        )
        query = self._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_connector_sync_by_type(self, connector_type: str) -> ConnectorSync | None:
        """Fetch the synchronization record (any status) for a connector type."""
        query = select(ConnectorSync).filter(ConnectorSync.connector_type == connector_type)
        query = self._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_connector_sync(
        self, connector_type: str, status: str, last_sync_time: datetime | None = None
    ) -> ConnectorSync:
        """Create or update a connector's synchronization status and timestamp."""
        sync = await self.get_connector_sync_by_type(connector_type)
        if sync:
            update_data = {"status": status}
            if last_sync_time:
                update_data["last_sync_time"] = last_sync_time
            # Apply manually so we use our base repo's validation
            return await self.update(sync, update_data)
        else:
            from app.core.context import get_current_tenant_id
            from app.core.exceptions import TenantIsolationError
            tenant_id = get_current_tenant_id()
            if not tenant_id:
                raise TenantIsolationError("Tenant context missing for connector sync creation.")

            new_sync = ConnectorSync(
                connector_type=connector_type,
                status=status,
                last_sync_time=last_sync_time,
                tenant_id=tenant_id
            )
            self.db.add(new_sync)
            await self.db.flush()
            return new_sync
