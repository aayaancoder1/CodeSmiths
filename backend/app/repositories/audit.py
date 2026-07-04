from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog
from app.repositories.base import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):
    """AuditRepository subclassing BaseRepository for logging compliance audits."""

    def __init__(self, db: AsyncSession):
        super().__init__(AuditLog, db)

    async def log_event(
        self,
        operation: str,
        status: str,
        user_id: UUID | None = None,
        document_id: UUID | None = None,
        details: Dict[str, Any] | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:
        """Create and store a new audit log entry."""
        log_data = {
            "operation": operation,
            "status": status,
            "user_id": user_id,
            "document_id": document_id,
            "details": details or {},
            "ip_address": ip_address,
        }
        # create method handles tenant ID injection automatically
        return await self.create(log_data)

    async def get_by_operation(self, operation: str, limit: int = 100) -> List[AuditLog]:
        """Fetch audit logs filtered by a specific operation name."""
        query = select(AuditLog).filter(AuditLog.operation == operation).order_by(AuditLog.timestamp.desc()).limit(limit)
        query = self._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_logs(
        self,
        user_id: UUID | None = None,
        document_id: UUID | None = None,
        operation: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AuditLog]:
        """Fetch audit logs with advanced filtering options, scoped by tenant."""
        query = select(AuditLog)
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if document_id:
            query = query.filter(AuditLog.document_id == document_id)
        if operation:
            query = query.filter(AuditLog.operation == operation)
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        
        query = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit)
        query = self._apply_tenant_filter(query)
        result = await self.db.execute(query)
        return list(result.scalars().all())

