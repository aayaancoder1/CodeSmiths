import asyncio
import logging
from datetime import datetime
from uuid import UUID
from celery import Task
from app.jobs.celery_app import celery_app
from app.config.config import settings

logger = logging.getLogger(__name__)


# Helper function to run async functions within Celery's sync worker thread context
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def sync_connector_task(self, tenant_id_str: str, connector_type: str, config: dict) -> dict:
    """Celery background task orchestrating incremental or full connector sync."""
    tenant_id = UUID(tenant_id_str)
    logger.info(f"Starting connector sync for tenant {tenant_id}, connector: {connector_type}")

    # Define async execution flow
    async def _execute():
        from app.db.session import async_session_maker
        from app.core.context import set_current_tenant_id
        from app.repositories.job import JobRepository
        from app.services.ingestion import IngestionService
        
        # 1. Establish tenant scope context for this thread/task
        set_current_tenant_id(tenant_id)

        async with async_session_maker() as db:
            job_repo = JobRepository(db)
            
            # Create a running Job record
            job = await job_repo.create({
                "job_type": f"connector_sync:{connector_type}",
                "status": "running"
            })
            await db.commit()

            try:
                # Update status of sync state in connector_syncs table
                await job_repo.update_connector_sync(connector_type, "syncing")
                await db.commit()

                # 2. Run ingestion sync
                ingestion_service = IngestionService(db)
                stats = await ingestion_service.sync_connector(connector_type, config)
                
                # 3. Mark job and connector sync status as completed
                await job_repo.update_job_status(job.id, "completed")
                await job_repo.update_connector_sync(connector_type, "idle", last_sync_time=datetime.utcnow())
                await db.commit()

                logger.info(f"Sync completed successfully. Ingested docs: {stats.get('ingested', 0)}, Errors: {stats.get('errors', 0)}")
                return {"status": "success", "job_id": str(job.id), "stats": stats}

            except Exception as e:
                logger.error(f"Sync task failed for tenant {tenant_id_str}: {e}")
                await db.rollback()
                
                # Update job tables
                await job_repo.update_job_status(job.id, "failed", error_message=str(e))
                await job_repo.update_connector_sync(connector_type, "failed")
                await db.commit()

                # Trigger Celery retry for transient network connectivity errors
                try:
                    self.retry(exc=e)
                except Exception as retry_err:
                    # If retries exceeded, raise original exception
                    raise retry_err
                
                raise e

    return run_async(_execute())


@celery_app.task
def cleanup_old_jobs_task() -> dict:
    """Scheduled task cleaning up completed/failed job logs older than 30 days."""
    logger.info("Starting background cleanup job.")

    async def _execute():
        from sqlalchemy import delete
        from app.db.session import async_session_maker
        from app.models.job import Job
        from app.models.audit import AuditLog
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        async with async_session_maker() as db:
            # 1. Clean old background jobs (Note: this deletes across all tenants, so we bypass tenant scoping check)
            jobs_delete = delete(Job).where(
                Job.created_at < cutoff_date,
                Job.status.in_(["completed", "failed"])
            )
            audit_delete = delete(AuditLog).where(
                AuditLog.timestamp < cutoff_date
            )
            
            job_res = await db.execute(jobs_delete)
            audit_res = await db.execute(audit_delete)
            await db.commit()
            
            return {
                "deleted_jobs": job_res.rowcount,
                "deleted_audit_logs": audit_res.rowcount
            }

    return run_async(_execute())


@celery_app.task
def reindex_tenant_documents_task(tenant_id_str: str) -> dict:
    """Asynchronous batch re-indexing job emitting events for all active documents in a tenant."""
    tenant_id = UUID(tenant_id_str)
    logger.info(f"Re-indexing documents for tenant {tenant_id}")

    async def _execute():
        from sqlalchemy import select
        from app.db.session import async_session_maker
        from app.core.context import set_current_tenant_id
        from app.models.document import Document
        from app.events.publisher import RedisEventPublisher, IndexingEvent
        
        set_current_tenant_id(tenant_id)
        publisher = RedisEventPublisher()
        
        async with async_session_maker() as db:
            query = select(Document).filter(Document.is_active == True, Document.tenant_id == tenant_id)
            result = await db.execute(query)
            documents = result.scalars().all()
            
            published_count = 0
            for doc in documents:
                event = IndexingEvent(
                    event_type="document.reindexed",
                    document_id=doc.id,
                    source=doc.source,
                    tenant_id=doc.tenant_id,
                    updated_at=datetime.utcnow(),
                    operation="update",
                    version=doc.current_version
                )
                await publisher.publish(event)
                published_count += 1
                
            return {"status": "success", "published_events_count": published_count}

    return run_async(_execute())
