from datetime import datetime
import uuid
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 Unified Declarative Base Class."""
    pass


class PrimaryKeyUUIDMixin:
    """Mixin defining a UUID primary key."""
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        sort_order=-10,  # Ensure ID comes first in table schemas
    )


class TenantIsolationMixin:
    """Mixin enforcing logical multi-tenancy with a tenant_id discriminator."""
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        sort_order=-9,  # Place tenant_id right after id
    )


class TimestampAuditMixin:
    """Mixin adding timezone-aware creation and update timestamps."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
