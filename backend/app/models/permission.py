import uuid
from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin


class Permission(Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin):
    """Representing an ACL permission linking a Document to a User or Group."""
    __tablename__ = "permissions"
    __table_args__ = (
        CheckConstraint(
            "(user_id IS NOT NULL AND group_id IS NULL) OR (user_id IS NULL AND group_id IS NOT NULL)",
            name="chk_permission_target_xor"
        ),
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True
    )
    group_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), nullable=True, index=True
    )
    # Permission levels: 'read', 'write', 'admin'
    level: Mapped[str] = mapped_column(String(50), nullable=False, default="read")

    # Relationships
    document: Mapped["Document"] = relationship("Document", back_populates="permissions")
    user: Mapped["User"] = relationship("User", lazy="selectin")
    group: Mapped["Group"] = relationship("Group", lazy="selectin")
