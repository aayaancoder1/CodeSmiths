import uuid
from typing import List
from sqlalchemy import ForeignKey, String, Text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin


class Document(Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin):
    """Representing an ingested document container."""
    __tablename__ = "documents"

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # e.g., 'google_drive', 'notion', 'upload'
    original_filename: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    current_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relationships
    versions: Mapped[List["DocumentVersion"]] = relationship(
        "DocumentVersion", back_populates="document", cascade="all, delete-orphan", passive_deletes=True
    )
    permissions: Mapped[List["Permission"]] = relationship(
        "Permission", back_populates="document", cascade="all, delete-orphan", passive_deletes=True
    )
    chunks: Mapped[List["Chunk"]] = relationship(
        "Chunk", back_populates="document", cascade="all, delete-orphan", passive_deletes=True
    )


class DocumentVersion(Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin):
    """Representing a specific version of an ingested document."""
    __tablename__ = "document_versions"

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    storage_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)  # Path to local/cloud backup file
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    document: Mapped[Document] = relationship("Document", back_populates="versions")
    chunks: Mapped[List["Chunk"]] = relationship(
        "Chunk", back_populates="version", cascade="all, delete-orphan", passive_deletes=True
    )


class Chunk(Base, PrimaryKeyUUIDMixin, TenantIsolationMixin, TimestampAuditMixin):
    """Representing parsed text splits from a specific document version."""
    __tablename__ = "chunks"

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("document_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    chunk_number: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    start_offset: Mapped[int] = mapped_column(Integer, nullable=False)  # Starting character offset in raw text
    end_offset: Mapped[int] = mapped_column(Integer, nullable=False)    # Ending character offset in raw text
    character_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    document: Mapped[Document] = relationship("Document", back_populates="chunks")
    version: Mapped[DocumentVersion] = relationship("DocumentVersion", back_populates="chunks")
