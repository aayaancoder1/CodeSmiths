import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.dependencies.context import get_tenant_id
from app.schemas.audit import AuditLogResponse
from app.repositories.audit import AuditRepository

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get(
    "",
    response_model=List[AuditLogResponse],
    summary="Retrieve compliance audit logs",
    description="Fetch security and modification audit trail logs scoped to the tenant. Supports advanced filtering."
)
async def get_audit_logs(
    user: Optional[uuid.UUID] = Query(None, description="Filter logs by requesting User UUID"),
    document: Optional[uuid.UUID] = Query(None, description="Filter logs by associated Document UUID"),
    operation: Optional[str] = Query(None, description="Filter logs by operation label (e.g. 'document.create')"),
    start_date: Optional[datetime] = Query(None, description="Filter logs starting from timestamp (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Filter logs up to timestamp (ISO format)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    audit_repo = AuditRepository(db)
    logs = await audit_repo.get_logs(
        user_id=user,
        document_id=document,
        operation=operation,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    return logs
