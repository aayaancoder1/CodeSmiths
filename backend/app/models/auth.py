import uuid
from typing import List
from sqlalchemy import Column, ForeignKey, String, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin

# Many-to-many join table for Users and Groups
user_groups = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
)

# Many-to-many join table for Users and Roles
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class Tenant(Base, PrimaryKeyUUIDMixin, TimestampAuditMixin):
    """Tenant representing an enterprise company/client."""
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class User(Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin):
    """User account associated with a specific tenant."""
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    groups: Mapped[List["Group"]] = relationship(
        secondary=user_groups, back_populates="users", lazy="selectin"
    )
    roles: Mapped[List["Role"]] = relationship(
        secondary=user_roles, back_populates="users", lazy="selectin"
    )


class Group(Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin):
    """Group of users for scaling permissions management within a tenant."""
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # Relationships
    users: Mapped[List[User]] = relationship(
        secondary=user_groups, back_populates="groups"
    )


class Role(Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin):
    """System role mapping to permission scopes for RBAC."""
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    # JSON array representing specific allowed system permissions, e.g. ["document:read", "admin:all"]
    scopes: Mapped[List[str]] = mapped_column(JSONB, default=list, nullable=False)

    # Relationships
    users: Mapped[List[User]] = relationship(
        secondary=user_roles, back_populates="roles"
    )
