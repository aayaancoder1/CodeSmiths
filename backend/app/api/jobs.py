import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.dependencies.context import get_tenant_id
from app.schemas.job import JobResponse
from app.repositories.job import JobRepository
from app.core.exceptions import EntityNotFoundError

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get(
    "/status",
    response_model=List[JobResponse],
    summary="List all tenant background jobs",
    description="Retrieve all background job logs scoped to the active tenant."
)
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    job_repo = JobRepository(db)
    jobs = await job_repo.get_multi(skip=skip, limit=limit)
    return jobs


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    summary="Get background job status",
    description="Query details and execution status of a specific background job."
)
async def get_job(
    job_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    tenant_id: uuid.UUID = Depends(get_tenant_id)
):
    job_repo = JobRepository(db)
    job = await job_repo.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job record with identifier {job_id} was not found."
        )
    return job
