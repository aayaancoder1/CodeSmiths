from datetime import datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin


class Job(Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin):
    """Job representing an execution instance of a background task."""
    __tablename__ = "jobs"

    job_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # e.g., 'connector_sync', 'reindex'
    # Job statuses: 'pending', 'running', 'completed', 'failed'
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)


class ConnectorSync(Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin):
    """ConnectorSync representing sync history and metrics for document integrations."""
    __tablename__ = "connector_syncs"

    connector_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # e.g., 'google_drive', 'notion'
    last_sync_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Sync status: 'idle', 'syncing', 'completed', 'failed'
    status: Mapped[str] = mapped_column(String(50), default="idle", nullable=False)
