import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.dependencies.context import get_tenant_id
from app.schemas.job import ConnectorSyncResponse, ConnectorSyncRequest
from app.repositories.job import JobRepository
from app.connectors import CONNECTOR_REGISTRY
from app.jobs.tasks import sync_connector_task

router = APIRouter(prefix="/connectors", tags=["Connectors"])


@router.get(
    "",
    response_model=List[str],
    summary="List available connectors",
    description="Retrieve list of all registered connector integration source keys."
)
async def list_connectors(tenant_id: uuid.UUID = Depends(get_tenant_id)):
    """Returns registry keys for configured connectable systems (Google Drive, Notion, Slack, Jira)."""
    return list(CONNECTOR_REGISTRY.keys())


@router.post(
    "/{connector}/sync",
    response_model=ConnectorSyncResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger connector sync",
    description="Queue a Celery task to synchronize external files incrementally into the ingestion pipeline."
)
async def sync_connector(
    connector: str,
    body: ConnectorSyncRequest,
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    """Triggers connector sync job, enforcing that only one sync of a type runs at a time per tenant."""
    if connector not in CONNECTOR_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Connector '{connector}' is not supported. Supported: {list(CONNECTOR_REGISTRY.keys())}"
        )

    job_repo = JobRepository(db)

    # Prevent concurrent syncs for the same connector type within the tenant
    active_sync = await job_repo.get_active_connector_sync(connector)
    if active_sync:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Connector '{connector}' synchronization is already running."
        )

    # Initialize / update state in DB to 'syncing'
    sync_record = await job_repo.update_connector_sync(connector, "syncing")
    await db.commit()
    await db.refresh(sync_record)

    # Dispatch Celery background task
    sync_connector_task.delay(str(tenant_id), connector, body.config)

    return sync_record
