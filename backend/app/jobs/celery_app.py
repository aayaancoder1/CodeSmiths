from celery import Celery
from app.config.config import settings

# Initialize Celery app bound to Redis broker
celery_app = Celery(
    "brain_jobs",
    broker=settings.BROKER_URL,
    backend=settings.RESULT_BACKEND,
)

# Enterprise configuration parameters
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=1800,           # 30-minute hard execution limit
    task_soft_time_limit=1500,      # 25-minute soft execution limit (allows soft cleanup)
    worker_prefetch_multiplier=1,   # Fetch only one document sync job at a time to prevent memory bloat
    task_acks_late=True,            # Acknowledge task completion only after successful execution (helps retry)
)

# Auto-discover task definitions inside the jobs folder
celery_app.autodiscover_tasks(["app.jobs"])
