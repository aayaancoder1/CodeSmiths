import uuid
from datetime import datetime
from typing import Any, Dict
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, PrimaryKeyUUIDMixin, TenantIsolationMixin


class AuditLog(Base, PrimaryKeyUUIDMixin, TenantIsolationMixin):
    """System and compliance audit logs."""
    __tablename__ = "audit_logs"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True, index=True
    )
    operation: Mapped[str] = mapped_column(String(255), nullable=False, index=True)  # e.g., 'document.ingest', 'permission.update'
    status: Mapped[str] = mapped_column(String(50), nullable=False)                  # 'success' or 'failure'
    details: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)        # Store IPv4 or IPv6

    # Relationships
    user: Mapped["User"] = relationship("User", lazy="selectin")
    document: Mapped["Document"] = relationship("Document", lazy="selectin")
